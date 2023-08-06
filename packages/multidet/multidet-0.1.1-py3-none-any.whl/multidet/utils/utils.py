import mxnet as mx
from matplotlib import colors as mcolors
import matplotlib
from itertools import zip_longest

class ctime():
    def __init__(self, prefix=''):
        self.prefix = prefix
    def __enter__(self, prefix=''):
        self.begin = time.time()
    def __exit__(self, *args):
        print(self.prefix, ': %.4f'%(time.time()-self.begin))
        

def get_gpu(num=4):
    ctx = []
    for i in range(num):
        try:
            tmp = mx.nd.zeros((1,), ctx=mx.gpu(i))
            ctx.append(mx.gpu(i))
        except mx.MXNetError:
            if len(ctx) == 0:
                ctx.append(mx.cpu())
            break
    return ctx


mean_rgb = mx.nd.array([123.68, 116.779, 103.939]).reshape((1,1,3))
std_rgb = mx.nd.array([58.393, 57.12, 57.375]).reshape((1,1,3))


# 用于画bbox时的颜色显示
colors = list(mcolors.cnames.values())


def getRecTex(bbox, label=None, bcolor='r', tcolor='w'):
    """
        根据bbox和label返回对应的patches和artist，
        用于后续在matplotlib中画图使用
    :param bbox: numpy，4个浮点值，对应左上角和右下角的xy
    :param label: str，要标注的text
    :param bcolor: str，bbox边框颜色
    :param tcolor: str，文本颜色
    :return:
    """
    rec = matplotlib.patches.Rectangle(
        xy=(bbox[0], bbox[1]), width=bbox[2] - bbox[0], height=bbox[3] - bbox[1],
        fill=False, edgecolor=bcolor, linewidth=3)
    
    if label is not None:
        tex = matplotlib.text.Text(bbox[0], bbox[1], label, color=tcolor,
                               verticalalignment='top', horizontalalignment='left',
                               fontsize=15, bbox=dict(facecolor=bcolor))
    # 如果没有传入label，那么另tex为None即可
    # 后续使用add_artist添加时也没问题
    else:
        tex = None
    return rec, tex


def showBBox(axes, img, bboxes, labels=None):
    """
        在axes上显示img和bbox及其label
    :param axes: 要显示图片的axes
    :param img: 要显示的图片，为numpy.array，要整数
    :param bboxes: 该图片的bbox们，(n, 4)，浮点数，numpy.array
                   为具体的两个点坐标，没有进行归一化的。
    :param labels: (n,) 对应类别的编号
    :return:
    """
    axes.imshow(img)
    h, w, c = img.shape
    if labels is None:
        labels = []
    if bboxes.ndim == 1:
        bboxes = [bboxes]
    for i, (bbox, label) in enumerate(zip_longest(bboxes, labels, fillvalue=None)):
        if label != -1:
            if label is not None:
                text = get_clsname(int(label))
                bcolor = colors[int(label)]
                tcolor = colors[int(label) + 100]
            else:
                text = ''
                bcolor = colors[i%100]
                tcolor = 'w'
 
            RecPatch, TexArt = getRecTex(bbox, text, bcolor=bcolor,
                                         tcolor=tcolor)
            axes.add_patch(RecPatch)
            axes.add_artist(TexArt)