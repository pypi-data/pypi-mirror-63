from mxnet.gluon import nn
import mxnet as mx

class BaseBlk(nn.HybridBlock):
    def __init__(self, init=None, use_bn=True, activation=None, **kwargs):
        super(BaseBlk, self).__init__(**kwargs)

        if init is None:
            self.init = {'weight_initializer': mx.init.Xavier(
                        rnd_type='gaussian', factor_type='in', magnitude=2),
                        'bias_initializer': 'zeros'}
        else:
            self.init = init

        if activation is None:
            self.act = 'relu'
        else:
            self.act = activation

        self.use_bn = use_bn


    def _get_conv(self, c, k, s, p=0, d=1, g=1):
        blk = nn.HybridSequential()
        blk.add(nn.Conv2D(channels=c, kernel_size=k, strides=s, padding=p, 
                          dilation=d, groups=g, use_bias=False, **self.init))
        if self.use_bn:
            blk.add(nn.BatchNorm())
        blk.add(nn.Activation(self.act))
        return blk

    def _get_dsc(self, in_ch, out_ch, s):
        blk = nn.HybridSequential()
        blk.add(self._get_conv(in_ch, 3, s, p=1, g=in_ch))
        blk.add(self._get_conv(out_ch, 1, 1))
        return blk

    def hybrid_forward(self, F, x):
        raise NotImplementedError

in_chs = [32, 64, 128, 128, 256, 256] + [512] * 6 + [1024]
out_chs = [64, 128, 128, 256, 256] + [512] * 6 +[1024] * 2
strides = [1, 2] * 3 + [1] * 5 + [2, 1]
config = [(ic, oc, s) for ic, oc, s in zip(in_chs, out_chs, strides)]

class MobileNet(BaseBlk):
    def __init__(self, wmul=1, classes=1000, config=config,
                 as_base=False, base_layer=None, **kwargs):
        super(MobileNet, self).__init__(**kwargs)
        self.as_base = as_base
        self.base_layer = base_layer

        with self.name_scope():
            self.features = nn.HybridSequential(prefix='')
            with self.features.name_scope():
                self.features.add(self._get_conv(int(32*wmul), 3, 2, 1))

                for ic, oc, s in config:
                    self.features.add(self._get_dsc(int(ic*wmul), int(oc*wmul), s))

                self.features.add(nn.GlobalAvgPool2D())
                self.features.add(nn.Flatten())

            self.output = nn.Dense(classes)

    def hybrid_forward(self, F, x):
        if self.as_base:
            output = []
            for i, blk in enumerate(self.features):
                x = blk(x)
                if i in self.base_layer:
                    output.append(x)
            x = self.output(x)
            if i+1 in self.base_layer:
                output.append(x)
            return output
        else:
            x = self.features(x)
            x = self.output(x)
            return x


def get_mobilenet(**kwargs):
    return MobileNet(config=config, **kwargs)