import mxnet as mx
import glob
from .genRecordIO import get_img, packLabelImg
import random
import os
from mxnet.gluon.data import dataset
from .image import *
from .classes import caltech256_cls
from .loadimg import Preprocess, ColorJitter, ShapeJitter


class Caltech(dataset.Dataset):
    CLASSES = caltech256_cls

    def __init__(self, rec_path, transform=None):
        super(Caltech, self).__init__()
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
        label = int(header.label)
        img = mx.nd.array(img, dtype='float32')

        if self._transform is not None:
            img = self._transform(img)

        return img, label    


class TrainTrans:
    def __init__(self):
        self.color = ColorJitter()
        self.shape = ShapeJitter()
        self.pre = Preprocess(rw=224, rh=224)

    def __call__(self, img):
        img = self.color(img)
        img = self.shape(img)
        img = self.pre(img)

        return img


class ValTrans:
    def __init__(self):
        self.pre = Preprocess()

    def __call__(self, img):
        img = self.pre(img)

        return img


class caltech256_2IO:
    def __init__(self, root=None, tv=0.8):
        self.classes = sorted([os.path.split(f)[-1] for f in \
                               glob.glob(os.path.join(root, '*'))])[:-1]

        self.root = root
        self.tv = tv

    def gen(self, path):
        train_rec = os.path.join(path, 'train_cal256.rec')
        train_idx = os.path.join(path, 'train_cal256.idx')
        train_rio = mx.recordio.MXIndexedRecordIO(train_idx, train_rec, 'w')

        val_rec = os.path.join(path, 'val_val256.rec')
        val_idx = os.path.join(path, 'val_val256.idx')
        val_rio = mx.recordio.MXIndexedRecordIO(val_idx, val_rec, 'w')

        self.train_num = 0
        self.val_num = 0
        for label, cls in enumerate(self.classes):
            imgs_path = glob.glob(os.path.join(self.root, cls, '*.jpg'))
            train_size = int(len(imgs_path) * self.tv)

            random.shuffle(imgs_path)

            train_path = imgs_path[:train_size]
            val_path = imgs_path[train_size:]

            for tpath in train_path:
                img = get_img(tpath)
                packio = packLabelImg(label, img)
                train_rio.write_idx(self.train_num, packio)
                self.train_num += 1

            for vpath in val_path:
                img = get_img(vpath)
                packio = packLabelImg(label, img)
                val_rio.write_idx(self.val_num, packio)
                self.val_num += 1

