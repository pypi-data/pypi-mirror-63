from .vgg_base import get_VGG16Feature
from .anchor import AnchorGenerator
from .coder import BoxDecoder, ClsDecoder
from mxnet.gluon import nn
from mxnet import nd
import mxnet as mx
import time

ratios = [[1, 2, 0.5], [1, 2, 0.5, 3, 1.0/3], [1, 2, 0.5, 3, 1.0/3], 
          [1, 2, 0.5, 3, 1.0/3], [1, 2, 0.5], [1, 2, 0.5]]

sizes = [30, 60, 111, 162, 213, 264, 315] 

steps = [8, 16, 32, 64, 100, 300]


class SSD(nn.HybridBlock):
    def __init__(self, img_size, base_net, scales, ratios, steps, num_cls=20,
                 stds=(0.1, 0.1, 0.2, 0.2), means=(0,0,0,0), asz=64, init=None,
                 amode='center', srmode='few', nms_thresh=0.45, nms_topk=400, 
                 post_nms=100, **kwargs):
        super(SSD, self).__init__(**kwargs)
    
        if init is None:
            # 激励函数使用的relu，所以使用He初始化方法
            # He配置为：rnd_type='gaussian', factor_type='in'(或'out'), 'magnitude'=2
            # Xavier配置为：rnd_type='uniform', factor_type='avg', 'magnitude'=3
            self.init = {'weight_initializer': mx.init.Xavier(
                        rnd_type='gaussian', factor_type='in', magnitude=2),
                        'bias_initializer': 'zeros'}
        else:
            self.init = init

        with self.name_scope():
            self.base_net = base_net(init=self.init)

        self.num_cls = num_cls
        self.img_size = img_size

        self.nms_thresh = nms_thresh
        self.nms_topk = nms_topk
        self.post_nms = post_nms

        scales = list(zip(scales[:-1], scales[1:]))
        assert len(scales) == len(ratios) 
        
        # 建立类别预测和偏移预测层
        self.cls_preds = nn.HybridSequential(prefix='cls_pred_')
        self.box_preds = nn.HybridSequential(prefix='box_pred_')
        self.anch_gens = nn.HybridSequential(prefix='anch_gen_')

        for i, (scale, ratio, step) in enumerate(zip(scales, ratios, steps)):
            with self.anch_gens.name_scope():
                anch_gen = AnchorGenerator(i, (self.img_size,self.img_size), 
                                              scale, ratio, step, (asz,asz),
                                              mode=amode, srmode=srmode)

            with self.cls_preds.name_scope():
                cls_pred = self._get_pred(anch_gen._depth, self.num_cls, mode='cls')
            
            with self.box_preds.name_scope():
                box_pred = self._get_pred(anch_gen._depth, mode='offset')

            self.cls_preds.add(cls_pred)
            self.box_preds.add(box_pred)
            self.anch_gens.add(anch_gen)
            # self.anch_gens.append(anch_gen)

        self.box_decoder = BoxDecoder(abox='center')
        self.cls_decoder = ClsDecoder(self.num_cls+1)

    def _get_pred(self, num_box, num_cls='', mode='cls', prefix=None):
        """
        根据传入的mode，确定是类别预测层还是偏移预测层。
        """
        assert mode in ('cls', 'offset')
        if mode == 'cls':
            channels = (num_cls + 1) * num_box
        else:
            channels = 4 * num_box
        # 输出层不要有激活函数
        blk = nn.Conv2D(channels, kernel_size=3, strides=1, padding=1, 
                        prefix=prefix, **self.init)
        return blk

    def set_nms(self, nms_thresh=0.45, nms_topk=400, post_nms=100):
        self.nms_thresh = nms_thresh
        self.nms_topk = nms_topk
        self.post_nms = post_nms
        
    def hybrid_forward(self, F, x):
        features = self.base_net(x)
        
        cls_preds = []
        offset_preds = []
        dboxes = []
        for f, clsp, boxp, anchg in zip(features, self.cls_preds, self.box_preds, self.anch_gens):
            cls_preds.append(clsp(f).transpose((0,2,3,1)).flatten())
            
            offset_preds.append(boxp(f).transpose((0,2,3,1)).flatten())
            
            dboxes.append(anchg(f).reshape((1, -1)))

        # (B, num_box, cls+1)
        cls_preds = F.concat(*cls_preds, dim=1).reshape((0, -1, self.num_cls+1))
        # (B, num_box*4) -> (B, N, 4)
        box_preds = F.concat(*offset_preds, dim=1).reshape((0, -1, 4))
        # (1, num_box, 4)
        anchors = F.concat(*dboxes, dim=1).reshape((1, -1, 4))

        if mx.autograd.is_training():
            return [cls_preds, box_preds, anchors]

        # (B,N,4)
        boxes = self.box_decoder(box_preds, anchors)
        # (B,N,C) (B,N,C)
        cls_ids, scores = self.cls_decoder(cls_preds)

        results = []
        for i in range(self.num_cls):
            # (B,N,1)
            cls_id = cls_ids.slice_axis(axis=-1, begin=i, end=i+1)
            # (B,N,1)
            score = scores.slice_axis(axis=-1, begin=i, end=i+1)
            # per class results
            # (B,N,6), （类别，分数，左上x，左上y，右下x，右下y）
            per_result = F.concat(*[cls_id, score, boxes], dim=-1)
            results.append(per_result)

        # C x (B,N,6) -> (B,CxN, 6)
        result = F.concat(*results, dim=1)

        if self.nms_thresh > 0 and self.nms_thresh < 1:
            # (B,CxN,6)
            result = F.contrib.box_nms(
                result, overlap_thresh=self.nms_thresh, topk=self.nms_topk, valid_thresh=0.01,
                id_index=0, score_index=1, coord_start=2, force_suppress=False)
            if self.post_nms > 0:
                # (B, post_nms, 6)
                result = result.slice_axis(axis=1, begin=0, end=self.post_nms)

        # (B, post_nms, 1)
        ids = F.slice_axis(result, axis=2, begin=0, end=1)
        # (B, post_nms, 1)
        scores = F.slice_axis(result, axis=2, begin=1, end=2)
        # (B, post_nms, 4)
        bboxes = F.slice_axis(result, axis=2, begin=2, end=6)

        return ids, scores, bboxes


def get_SSD300():
    """
    no parameter, just call it
    """
    base_net = get_VGG16Feature
    ssd = SSD(300, base_net, sizes, ratios, steps)
    return ssd