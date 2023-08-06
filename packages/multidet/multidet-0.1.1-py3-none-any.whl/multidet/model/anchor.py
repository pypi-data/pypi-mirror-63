from mxnet import nd
from mxnet.gluon import nn
import math


def getAnchorWH(scales, ratios, srmode='few'):
    """
        根据scales和ratios生成box的宽和高。
        srmode用于指定scales和ratios的组合形式。
        各特征图上每个cell具有的box形状一致，所以这里就生成这些形状的宽高。
    输入：
        scales: 为处理好的一维NDArray
        ratios: 为处理好的一维NDArray
        fw: 特征图宽度
        fh: 特征图高度
        srmode: 
            'few': 只生成scales[0]和ratios以及scales[1:]和ratios[0]的box尺寸
            'many': 生成scales和所有ratios组合的box尺寸
    输出：
        width: 所有高度，为一维NDArray形式
        height: 对应的宽度，为一维NDArray形式
    """
    assert srmode in ('few', 'many')
    if srmode == 'few':
        # box的尺寸数量
        num = scales.size + ratios.size - 1
        # 用于存入各尺寸对应的宽高
        width = nd.zeros((num,))
        height = nd.zeros((num,))
        
        # 先将ratios中的值开方，以待后续使用
        sqt_ratios = nd.sqrt(ratios)

        # 先是ratios[0]与所有scale搭配
        width[:scales.size] = scales * sqt_ratios[0]
        height[:scales.size] = scales / sqt_ratios[0]
        # 然后是scales[0]与ratios[1:]搭配
        width[scales.size:] = scales[0] * sqt_ratios[1:]
        height[scales.size:] = scales[0] / sqt_ratios[1:]


    else:
        num = scales.size * ratios.size
        # 先是scales[0]与ratios，然后是scales[1]与ratios.....
        # nd.repeat是对每个元素进行重复
        # ratios.size个scales[0], ratios.size个scales[1],
        # ratios.size个scales[2], ratios.size个scales[2],......
        rscales = nd.repeat(scales, ratios.size)
        # nd.tile是将数组作为整体重复
        # scales.size个ratios
        rratios = nd.tile(ratios, scales.size)
        
        # 就是按元素乘除
        width = rscales * nd.sqrt(rratios)
        height = width / rratios

    # (num, 2)
    wh = nd.stack(width, height, axis=1)
    
    return wh, num


def generate_anchor(sizes, ratios, step, alloc_size, 
                    offsets=(0.5, 0.5), mode='center', srmode='few'):
    """
        生成anchor。
    输入：
        sizes: 一维NDArray
        ratios: 一维NDArray
        step: 投射到原图上的尺度
        alloc_size: 假设是在这个尺度的特征图上生成
        srmode: 'few'或'many'，'few'只生成len(scales)+len(ratios)-1个，
              'many'生成len(scales)*len(ratios)个
              
        offset: 两元素列表，分别为xy偏移。默认为[0.5, 0.5]
        
    """

    assert mode in ('corner', 'center')
    fh, fw = alloc_size
    # (num, 2)
    wh, num = getAnchorWH(sizes, ratios, srmode=srmode)

    # (fh, fw)
    xpoints = nd.repeat(nd.arange(fw).reshape((1,-1)), fh, axis=0) + offsets[1]
    ypoints = nd.repeat(nd.arange(fh).reshape((-1,1)), fw, axis=1) + offsets[0]
    # (fh, fw, 2) -> (1, fhxfw, 2)
    xycenters = nd.stack(xpoints, ypoints, axis=2).reshape((1,-1,2)) * step
    
    if mode == 'center':
        # (num, 2) -> (1, fhxfwxnum, 2)
        wh = nd.tile(wh, (1, fh*fw, 1))
        # (1, fhxfw, 2) -> (1, fhxfwxnum, 2)
        xycenters = nd.repeat(xycenters, num, axis=1)
        # (1,fhxfwxnum,4)
        xycenters = nd.concat(xycenters, wh, dim=2)
    else:
        # (1, fhxfw, 2) -> (1, fhxfw, 4xnum)
        xycenters = nd.tile(xycenters, (1,1,2*num))
        # (num, 2) -> (num, 4) -> (1,1,4xnum)
        wh = nd.concat(wh*-0.5, wh*0.5, dim=1).reshape((1,1,-1))
        # (1, fhxfw, 4xnum)
        xycenters = xycenters + wh

    # (1,1,fh,fw,numx4)
    xycenters = xycenters.reshape((1,1,fh,fw,-1))

    return xycenters, num


class AnchorGenerator(nn.HybridBlock):
    """
    生成anchor，在定义时生成，具体多少在forward中根据输入确定。
    """
    def __init__(self, index, im_size, sizes, ratios, step, 
                            #(h,w)
                 alloc_size=(64, 64), offsets=(0.5, 0.5), 
                 # center模式的clip无意义
                 # corner的还有点意义
                 # 待补全
                 clip=False, mode='center', srmode='few', **kwargs):
        super(AnchorGenerator, self).__init__(**kwargs)
        self._im_size = im_size
        self._clip = clip
        self._sizes = (sizes[0], math.sqrt(sizes[0] * sizes[1]))
    
        # (1,1,fh,fw,numx4)
        anchors, self._depth = generate_anchor(nd.array(self._sizes), 
                                               nd.array(ratios), 
                                              step, alloc_size, offsets=offsets, 
                                               srmode=srmode, mode=mode)
    
        self.anchors = self.params.get_constant('anchor_%d'%(index), anchors)

    def hybrid_forward(self, F, x, anchors):
        anchor = F.slice_like(anchors, x, axes=(2,3))
        return anchor.reshape((1, -1, 4))




