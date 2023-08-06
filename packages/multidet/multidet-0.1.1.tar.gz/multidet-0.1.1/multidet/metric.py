import mxnet as mx
from mxnet.gluon import utils as gutils

def classify_acc(net, val_iter, ctx=None):
    """
    在验证集上统计分类模型的测量精度
    后续补充功能：统计各类别的测量精度
    """
    total_acc = 0
    num_sample = 0

    if ctx is None:
        ctx = mx.cpu()

    for X, y in val_iter:
        Xs = gutils.split_and_load(X, ctx_list=ctx, batch_axis=0)
        ys = gutils.split_and_load(y, ctx_list=ctx, batch_axis=0)
        
        y_hats = []
        for data in Xs:
            y_hat = net(data)
            y_hats.append(y_hat)

        for y_hat, label in zip(y_hats, ys):
            total_acc += (y_hat.argmax(axis=-1) == label.astype(y_hat.dtype)).sum().asscalar()
            num_sample += len(label)

    return total_acc / num_sample
