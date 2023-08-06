"""
该文件定义了数据集读取序列类型。以及用于该类型实例的transform类。
"""
import numpy as np
import random
import mxnet as mx
from mxnet.gluon.data import dataset
import os
from .image import *
from mxnet.gluon.data.vision.transforms import Compose
from ..model.box import *


class VOCDataset(dataset.Dataset):

    CLASSES = ('aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
               'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
               'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor')

    def __init__(self, rec_path, transform=None):
        super(VOCDataset, self).__init__()
        self.rec_path = rec_path
        self.idx_path = os.path.splitext(rec_path)[0] + '.idx'

        # 注意了，不要覆盖父类方法
        self._transform = transform

        self.recordio = mx.recordio.MXIndexedRecordIO(self.idx_path, self.rec_path, 'r')

    @property
    def classes(self):
        return type(self).CLASSES

    def __len__(self):
        return len(self.recordio.keys)

    def __getitem__(self, idx):
        record = self.recordio.read_idx(self.recordio.keys[idx])
        header, img = mx.recordio.unpack_img(record)

        # 提取label信息
        headlen = int(header.label[0])  # 添加信息长度
        labellen = int(header.label[1])  # 每个bbox标注长度

        # 图片是NDArray，label为ndarray
        label = header.label[headlen:].reshape((-1, labellen)).copy()
        img = mx.nd.array(img, dtype='float32')

        if self._transform is not None:
            img, label = self._transform(img, label)

        return img, label


class ColorJitter:
    def __init__(self, brightness=50, contrast=0.5, saturation=0.5,
                 hue=18, p=0.5):
        self.b = brightness
        self.c = contrast
        self.s = saturation
        self.h = hue
        self.p = p

    def __call__(self, img):
        img = color_jitter(img, brightness=self.b, contrast=self.c, 
                           saturation=self.s, hue=self.h, p=self.p)

        return img


class ShapeJitter:
    def __init__(self, mean=(0.485, 0.456, 0.406)):
        self.mean = mean
    def __call__(self, img, label=None):
        if label is None:
            img = random_crop(img)
            img = flip(img, px=0.7)
            return img

        if random.uniform(0,1) > 0.7:
            img, label = expand_border(img, label, 
                         fill_value=[255*i for i in self.mean])

        img, label = random_crop_det(img, label, size=(0.1,1), ratio=(1/2,2), 
                          min_overlaps=(0.1,0.3,0.5,0.7,0.9), max_tmp=30)

        img, label = flip(img, label, px=1)

        return img, label


class Preprocess:
    def __init__(self, rw=300, rh=300, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        self.rw = rw
        self.rh = rh
        self.mean = mean
        self.std = std

    def __call__(self, img, label=None):
        if label is not None:
            img, label = resize(img, self.rw, self.rh, label)
        else:
            img = resize(img, self.rw, self.rh)
        img = to_tensor(img)
        img = normalize(img, mean=self.mean, std=self.std)

        return (img, label) if label is not None else img


class TargetGen:
    def __init__(self, anchors):
        self.anchors = anchors

    def __call__(self, label):
        gt_bboxes = mx.nd.array(label[np.newaxis, :, :4])
        gt_ids = mx.nd.array(label[np.newaxis, :, 4])
        
        anchors = BoxConverter(beh='2corner')(self.anchors.reshape((-1, 4)))
        iou = calIOU(anchors, gt_bboxes)
        mat = match(iou, threshould=0.5, share_max=False)
        samp = sample(mat, None, iou, ratio=3, min_sample=0, threshold=0.3, do=False)
        label_cls = label_box_cls(mat, samp, gt_ids, ignore_label=-1)
        anchor_offset, _ = label_offset(anchors, gt_bboxes, mat, samp, flatten=False)
        
        return label_cls[0], anchor_offset[0]


class TrainTrans:
    def __init__(self, anchor):
        self.anchor = anchor
        self.color = ColorJitter()
        self.shape = ShapeJitter()
        self.pre = Preprocess()
        self.label = TargetGen(anchor)

    def __call__(self, img, label):
        img = self.color(img)
        img, label = self.shape(img, label)
        img, label = self.pre(img, label)

        cls_target, box_target = self.label(label)

        return img, cls_target, box_target

class ValTrans:
    def __init__(self):
        self.pre = Preprocess()

    def __call__(self, img, label):
        img, label = self.pre(img, label)

        return img, label


def tbatchify_fn(data):
    """
    用于训练集DataLoader中的batchify_fn。
    将data中各维数据打包为一batch。
    data为list，形式为：
        [(img, cls_target, box_target),
         (img, cls_target, box_target),
         (img, cls_target, box_target),...,]
    返回result为list，形式为：[imgs, cls_targets, box_targets]
    """
    result = []
    for i in range(len(data[0])):
        result.append(nd.stack(*[d[i] for d in data], axis=0))
    return result


def vbatchify_fn(data):
    """
    用于验证集DataLoader中的batchify_fn。
    将data各维数据打包为一batch。对于第二维要进行pad -1。
    data为列表，形式为：
        [(img, label),
         (img, label),
         (img, label),...,]
    返回result为list，形式为：[imgs, labels]
    """
    result = []
    result.append(nd.stack(*[d[0] for d in data], axis=0))
    
    B = len(data)
    row_num, col_num = data[0][1].shape
    for d in data:
        r, c = d[1].shape
        if r > row_num:
            row_num = r
            
    dist = nd.full((B, row_num, col_num), -1)
    for i, d in enumerate(data):
        r, c = d[1].shape
        dist[i,:r,:c] = d[1]
    
    result.append(dist)
    return result




#######################################################################

# 值进行了随机裁剪的Augmenter
default_auglist = mx.image.CreateDetAugmenter((3,300,300),
                                              rand_crop=0.5, mean=None, std=None,
                                              min_object_covered=[0.7, 0.9])
# 不光进行了裁剪，还对图片进行了归一化处理
auglist = mx.image.CreateDetAugmenter((3,300,300),
                                      rand_crop=0.5, mean=True, std=True,
                                      min_object_covered=0.95)

auglist_full = mx.image.CreateDetAugmenter((3,300,300),
                rand_crop=0.5, mean=True, std=True,
                min_object_covered=[0.7, 0.9], brightness=0.125,
                contrast=0.125, saturation=0.125)


class DataIter:
    """
        自定义的迭代器类型，根据recordio文件.idx和.rec，来不断生成imgs和labels。
        根据cur和flag指示当前状态。如果当前读完后，到头了，设置flag，但要等到下一次
        读取的时候再抛出stopiteration异常，并复位状态。
    """
    def __init__(self, idx, rec, batch_size, shuffle=False, aug_list=None, ctx=None):
        self.recordio = mx.recordio.MXIndexedRecordIO(idx, rec, 'r')
        self.indexes = self.recordio.keys
        self.num_img = len(self.indexes)
        self.batch_size = batch_size
        self.aug_list = aug_list
        self.ctx = ctx
        self.shuffle = shuffle

        self.rand_indexes = self.indexes.copy()
        self.reset()

    def _sample_from_ind(self, ind, aug_list=None):
        """
        根据ind提取record，并根据aug_list中的Augmenter对图片及标注进行处理
        """
        record = self.recordio.read_idx(ind)
        header, img = mx.recordio.unpack_img(record)
        # 转为RGB，在通道维上倒序即可
        img = img[:, :, ::-1]

        # 提取label信息
        headlen = int(header.label[0])  # 添加信息长度
        labellen = int(header.label[1])  # 每个bbox标注长度
        numbox = int(header.label[2])  # 有多少是有效bbox

        # 各Augmenter需要输入图片是NDArray，label为ndarray
        label = header.label[headlen:].reshape((-1, labellen))
        img = mx.nd.array(img, ctx=self.ctx)

        if aug_list is not None:
            # dtype很重要，不然默认是uint8！！！
            # aug会对图片及其label作出变换
            olabel = np.full(label.shape, -1, dtype='float32')
            # 假label中的多个-1，可能会造成数值上的错误，
            # 所以这边将其过滤出来。
            labeltmp = label[:numbox]
            for aug in aug_list:
                # 有的Augmenter可能会减少标注bbox的数量
                img, labeltmp = aug(img, labeltmp)
            if labeltmp.shape[0] == 0:
                labeltmp = label[:numbox]
            olabel[:labeltmp.shape[0]] = labeltmp
            label = olabel

        label = mx.nd.array(label, ctx=self.ctx)
        return img.transpose((2, 0, 1)), label

    

    def next_sample(self, aug_list=None):
        """
        不断提取下一个图片，如果到头抛出StopIteration异常
        刚到头的时候，设置标志位，但并不抛出。
        设置标志位后，如果还要读取，就抛出。抛前清除状态，为下一次迭代准备。
        """
        if self.flag:
            self.reset()
            raise StopIteration

        img, label = self._sample_from_ind(self.rand_indexes[self.cur],
                                           aug_list=aug_list)
        self.cur += 1
        if self.cur >= self.num_img:
            self.flag = 1

        return img, label

    def next_batch(self):
        labels = []
        imgs = []

        i = 0
        while i < self.batch_size:
            img, label = self.next_sample(aug_list=self.aug_list)
            imgs.append(img)
            labels.append(label)
            i += 1
            # 对于最后一batch，如果数量不足，就不足吧
            if self.cur >= self.num_img:
                break
        # 都是NDArray格式
        return mx.nd.stack(*imgs, axis=0), mx.nd.stack(*labels, axis=0)

    def tell(self):
        return self.cur

    def reset(self):
        self.cur = 0
        self.flag = 0
        if self.shuffle:
            random.shuffle(self.rand_indexes)

    def __next__(self):
        return self.next_batch()

    def __iter__(self):
        return self