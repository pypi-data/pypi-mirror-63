# 自定义激励函数
from mxnet.gluon import nn
from mxnet import autograd, init

__all__ = ['MyReLU', 'MyLeakyReLU', 'MyRReLU', 'MyPReLU', 'MyELU', 'MySELU']


class MyReLU(nn.HybridBlock):
    def __init__(self):
        super(MyReLU, self).__init__()
        
    def hybrid_forward(self, F, x):
        return F.maximum(0, x)


class MyLeakyReLU(nn.HybridBlock):
    def __init__(self, alpha):
        super(MyLeakyReLU, self).__init__()
        self.alpha = alpha
        
    def hybrid_forward(self, F, x):
        return F.where(x < 0, F.broadcast_mul(self.alpha, x), x)


class MyRReLU(nn.HybridBlock):
    def __init__(self, low=0.01, high=0.2):
        super(MyRReLU, self).__init__()
        self.low = low
        self.high = high
        self.center = (low + high) / 2
        
    def hybrid_forward(self, F, x):
        if autograd.is_training():
            alpha = F.random.uniform(low=self.low, high=self.high, shape=1)
        else:
            alpha = self.center
        return F.where(x < 0, F.broadcast_mul(alpha, x), x)


class MyPReLU(nn.HybridBlock):
    def __init__(self, init=init.Constant(0.25), in_channels=1):
        super(MyPReLU, self).__init__()
        if in_channels != 1:
            shape = (1, in_channels, 1, 1)
        else:
            shape = (1,)
        with self.name_scope():
            self.alpha = self.params.get('alpha', shape=shape,
                                         init=init)
            
    def hybrid_forward(self, F, x, alpha):
        return F.where(x < 0, F.broadcast_mul(alpha, x), x)


class MyELU(nn.HybridBlock):
    def __init__(self, alpha):
        super(MyELU, self).__init__()
        self.alpha = alpha
    
    def hybrid_forward(self, F, x):
        return F.where(x < 0, self.alpha * (F.exp(x) - 1), x)



class MySELU(nn.HybridBlock):
    def __init__(self, scale=1.0507009873554804934193349852946,
                       alpha=1.6732632423543772848170429916717):
        super(MySELU, self).__init__()
        self.scale = scale
        self.alpha = alpha
        
    def hybrid_forward(self, F, x):
        return self.scale * F.where(x < 0, self.alpha * (F.exp(x) - 1), x)