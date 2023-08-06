from mxnet.gluon import nn

# 不同的loss实现需要搭配不同的trainer.step() ！！！！！！！！
class SSDLoss(nn.HybridBlock):
    """
    SSD训练中的loss。类别使用softmax，偏移使用SmoothL1。
    类别loss使用正类+负类，偏移loss只用正类。
    可在这里进行负采样。如果在这里进行负采样，那么在类别标注之前就不要进行负采样了。
    """
    def __init__(self, ratio=3, min_sample=0, rho=1.0, lambd=1.0, **kwargs):
        super(SSDLoss, self).__init__(**kwargs)
        # 负box与正box的数量之比
        self._ratio = max(0, ratio)
        # 最少从负box中采样出多少负box
        self._min_sample = max(0, min_sample)
        # smooth l1参数
        self._rho = rho
        # loc loss权重
        self._lambd = lambd

    def hybrid_forward(self, F, cls_preds, cls_targets, box_preds, box_targets):
        """
        cls_preds: (B,N,C+1)，预测的box类别
        cls_targets: (B,N), 对box标注的类别，为0～C+1，若存在-1，当0对待.0为背景，即负box
        box_preds: (B,N,4)，对box偏移的预测
        box_targets: (B,N,4), 对box偏移的标注
        """
#########################################################################
        # 1. class loss
        # (B,N,C+1)，先得到各个类别的log_softmax
        losses = F.log_softmax(cls_preds, axis=-1)
        # (B,N)，然后根据cls_target来pick一下，在乘以-1
        # 便得到各个box的类别loss。
        losses = -1 * F.pick(losses, cls_targets, axis=-1, keepdims=False)
        # (B,N)，正box的掩码
        mask = cls_targets > 0
        # (B,1)，各sample中有多少正box
        num_pos = F.sum(mask, axis=-1, keepdims=True)
        # (B,1)，除正box外，有多少负box
        max_neg = F.sum(F.ones_like(mask), axis=-1, keepdims=True) - num_pos
        # (B,1)，根据采样比率、最少采样数、负box最多个数，得到最终的要采样出的负box个数
        num_neg = F.minimum(F.maximum(self._min_sample, num_pos * self._ratio),
                            max_neg)
        # 下面要根据各负box的类别loss，进行负采样                    
        # (B,N), 这里很巧妙。先将正box的loss乘0，负box的loss乘-1.
        # 然后得到值最小的num_neg个乘以-1了的负box的loss的掩码。
        sample_indx = F.argsort(F.argsort(losses * (mask-1), axis=-1), axis=-1) 
        # (B,N)
        sample_mask = F.broadcast_lesser(sample_indx, num_neg)
        # 现在的总mask中值为1的地方表示正box和被采样出来的负box。
        # 对于conf loss，只计算这些。
        total_mask = (mask+sample_mask) > 0
        # (B,N)，掩一下
        target_closs = F.where(total_mask, losses, F.zeros_like(losses))
        
        # (B,1)
        # 1. 搭配bloss1. trainer.step(batch_size). epoch0后的map为0.193，gluoncv中的版本epoch0后map为0.142.
        target_closs = F.broadcast_div(F.sum(target_closs, axis=1, keepdims=True), F.maximum(num_pos, 1)) 
        # 2. 搭配bloss2. trainer.step(num_gpu). epoch0后的map为0.13, epoch1的map为0.353
        # target_closs = F.broadcast_div(F.sum(target_closs), F.sum(num_pos))  
        # 3. 搭配bloss3. trainer.step(num_gpu), epoch0的map为0.192，epoch1的map为0.387                           
        # target_closs = F.broadcast_div(F.sum(target_closs, axis=1, keepdims=True), F.sum(num_pos))      

        # (B,) 
        target_closs = F.squeeze(target_closs)

#########################################################################
        # 2. box loss 
        # (B, N, 4)
        abs_loss = F.abs(box_preds - box_targets)
        # (B, N, 4)
        smooth_loss = F.where(abs_loss > self._rho, abs_loss - 0.5 * self._rho,
                              (0.5 / self._rho) * F.square(abs_loss))
        # (B, N, 4)
        target_bloss = F.broadcast_mul(smooth_loss, F.expand_dims(mask, axis=2))
        
        # (B,)
        # 1.
        target_bloss = F.broadcast_div(F.sum(target_bloss, axis=0, exclude=True), F.squeeze(F.maximum(num_pos, 1))) 
        # 2
        # target_bloss = F.broadcast_div(F.sum(target_bloss), F.sum(num_pos)) 
        # 3
        # target_bloss = F.broadcast_div(F.sum(target_bloss, axis=0, exclude=True), F.sum(num_pos)) 
        
        # total
        total_loss = target_closs + self._lambd * target_bloss

        return total_loss, target_closs, target_bloss