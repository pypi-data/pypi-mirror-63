from mxnet import nd
from mxnet.gluon import nn
from .box import BoxConverter

class BoxDecoder(nn.HybridBlock):
    def __init__(self, means=(0,0,0,0), stds=(0.1,0.1,0.2,0.2),
                 # 是指输入anchor的形式
                 abox='center', **kwargs):
        super(BoxDecoder, self).__init__(**kwargs)
        assert abox in ('center', 'corner')

        if abox == 'corner':
            # 如果是corner的anchor，需要将其转为center形式
            self.convter = BoxConverter(beh='2center', split=True)
        else:
            self.convter = BoxConverter(beh=None, split=True)

        self.means = means
        self.stds = stds

    def hybrid_forward(self, F, x, anchors):
        """
        对预测的anchor偏移进行解码，得到修正后的anchor坐标
        anchor坐标形式为(x, y, w, h)
        输入：
            x: box_preds (B,N,4)
            anchors: (1,N,4)
        输出：
            decode: (B,N,4)
        """
        # (1,N,4) -> 4 x (1,N,1), to center mode
        a = self.convter(anchors)
        # (B,N,4) -> 4 x (B,N,1)
        p = F.split(x, num_outputs=4, axis=-1)

        x = F.broadcast_add(F.broadcast_mul((p[0] * self.stds[0] + self.means[0]), a[2]), a[0])
        y = F.broadcast_add(F.broadcast_mul((p[1] * self.stds[1] + self.means[1]), a[3]), a[1])

        w = F.broadcast_mul(F.exp(p[2] * self.stds[2] + self.means[2]), a[2]) / 2
        h = F.broadcast_mul(F.exp(p[3] * self.stds[3] + self.means[3]), a[3]) / 2

        return F.concat(x-w, y-h, x+w, y+h, dim=-1)


class ClsDecoder(nn.HybridBlock):
    def __init__(self, num_cls, axis=-1, thresh=0.01):
        """
        根据网络对每一个anchor的各类别预测，输出分数大于thresh的所有类别的分数和类别号。
        小于thresh的类别标记为-1，分数为0.
        - axis：各类别的预测维度
        - thresh: softmax之后的分数阈值，分数低于该值的输出类别标为-1，分数标为0
        """
        super(ClsDecoder, self).__init__()
        self._fg_class = num_cls - 1
        self._axis = axis
        self._thresh = thresh

    def hybrid_forward(self, F, x):
        """
        input:
        - x: cls_pred, (B,N,C+1)，网络类别预测输出
        output:
        - cls_id：（B,N,C)，不包含背景的类别编号，从0开始，-1表示为该类别分数小于thresh
        - scores：（B,N,C)，对应的各类别的分数，0表示该类别的分数小于thresh
        """
        # 先对预测转为softmax分数
        cls_pred = F.softmax(x, axis=self._axis)
        # (B,N,C) 除背景外的类别分数
        fore_score = F.slice_axis(cls_pred, axis=self._axis, begin=1, end=None)
        # (B,N,1)
        template = F.zeros_like(x.slice_axis(axis=-1, begin=0, end=1))
        # (B,N,C)
        cls_id = F.broadcast_add(template,
                                    # (1,1,C)
                                 F.reshape(F.arange(self._fg_class), shape=(1, 1, self._fg_class)))
        # (B,N,C)
        mask = fore_score > self._thresh
        cls_id = F.where(mask, cls_id, F.ones_like(cls_id) * -1)
        fore_score = F.where(mask, fore_score, F.zeros_like(fore_score))
        return cls_id, fore_score


def NMS(cls_ids, scores, boxes, overlap_thresh=0.5, topk=100, 
        valid_thresh=0.01, consider_cls=False):
    """
    input:
        cls_ids: (B,N)
        scores:  (B,N)
        boxes:   (B,N,4), corner
    """
    result = []
    #   (N,)    (N,)   (N,4)
    for cls_id, score, box in zip(cls_ids, scores, boxes):
        mask = score > valid_thresh
        valid_box_num = mask.sum()

        if topk > 0:
            valid_box_num = nd.minimum(valid_box_num, topk)

        arg_max = nd.argsort(score, axis=0, is_ascend=False)
        arg_max = arg_max[:valid_box_num.asscalar()]
        
        indx = []
        while len(arg_max) > 0:
            indx.append(arg_max[0])
            if len(arg_max) == 1:
                break
            idx = arg_max[0]
            arg_max = arg_max[1:]
            
            top_left = nd.maximum(box[idx, :2], box[arg_max, :2])
            bottom_right = nd.minimum(box[idx, 2:4], box[arg_max, 2:4])
            wh = nd.maximum(0, bottom_right-top_left)
            inter = nd.prod(wh, axis=-1)

            iou = inter / (nd.prod(box[idx, 2:4]-box[idx, :2], axis=-1) +
                           nd.prod(box[arg_max, 2:4]-box[arg_max, :2], axis=-1) -
                           inter)

            mask = iou <= overlap_thresh

            if consider_cls:
                cur_id = cls_id[idx]
                ids = cls_id[arg_max]
                mask = nd.logical_or(mask, nd.not_equal(cur_id, ids).astype('float32'))
            
            num = nd.sum(mask)
            least = nd.where(mask, arg_max, nd.zeros_like(arg_max))
            tmp = nd.arange(len(arg_max)) 
            tmp = tmp * mask
            tmp = nd.sort(tmp)[-int(num.asscalar()):]
            arg_max = nd.take(least, axis=0, indices=tmp)

        idx = nd.concat(*indx, dim=0)
        target_id = nd.take(cls_id, indices=idx, axis=0)
        target_score = nd.take(score, indices=idx, axis=0)
        target_box = nd.take(box, indices=idx, axis=0)
        
        result.append((target_id, target_score, target_box))
        
    return result
