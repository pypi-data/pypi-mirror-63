import random
import mxnet as mx
import numpy as np
import numbers
from ..model.box import calIOU_np


def random_gray(img, p=0.5):
    if random.uniform(0, 1) > p:
        img = img * mx.nd.array([[[0.299, 0.587, 0.114]]])
        img = img.sum(axis=2, keepdims=True)
        img = mx.nd.concat(img, img, img, dim=2)
        return img
    return img


def contrast_brightness(img, c=0.5, b=50, p=0.5):
    if random.uniform(0, 1) > p:
        sigma = random.uniform(-b, b)
        img += sigma

    if random.uniform(0, 1) > p:
        delta = random.uniform(1-c, 1+c)
        img *= delta

    img = mx.nd.clip(img, 0, 255)
    return img


def random_saturation(img, c=0.5, p=0.5):
    if random.uniform(0, 1) > p:
        alpha = random.uniform(1-c, 1+c)
        gray = img * mx.nd.array([[[0.299, 0.587, 0.114]]])
        gray = mx.nd.sum(gray, axis=2, keepdims=True)
        gray *= (1.0 - alpha)
        img *= alpha
        img += gray
        img = mx.nd.clip(img, 0, 255)
        return img
    return img


def random_hue(img, delta=18, p=0.5):
    """Augmenter body.
       Using approximate linear transfomation described in:
       https://beesbuzz.biz/code/hsv_color_transforms.php
    """
    if random.uniform(0, 1) > p:
        alpha = random.uniform(-delta, delta)

        u = np.cos(alpha * np.pi)
        w = np.sin(alpha * np.pi)

        bt = np.array([[1.0, 0.0, 0.0],
                       [0.0, u, -w],
                       [0.0, w, u]])
        tyiq = np.array([[0.299, 0.587, 0.114],
                         [0.596, -0.274, -0.321],
                         [0.211, -0.523, 0.311]])
        ityiq = np.array([[1.0, 0.956, 0.621],
                          [1.0, -0.272, -0.647],
                          [1.0, -1.107, 1.705]])
        t = np.dot(np.dot(ityiq, bt), tyiq).T
        img = mx.nd.dot(img, mx.nd.array(t))
        img = mx.nd.clip(img, 0, 255)
        return img
    return img


def expand_border(img, label=None, ratio_max=1.5, fill_value=255, keep_ratio=True):
    assert ratio_max > 1

    h, w, c = img.shape

    ratio_x = random.uniform(1, ratio_max)

    if keep_ratio:
        ratio_y = ratio_x
    else:
        ratio_y = random.uniform(1, ratio_max)

    oh, ow = int(h * ratio_y), int(w * ratio_x)

    off_y = random.randint(0, oh - h)
    off_x = random.randint(0, ow - w)

    if isinstance(fill_value, numbers.Number):
        dst = mx.nd.full(shape=(oh, ow, c), val=fill_value, dtype=img.dtype)
    else:
        fill = mx.nd.array(fill_value, dtype=img.dtype)
        dst = mx.nd.tile(fill.reshape((1, 1, c)), reps=(oh, ow, 1))

    dst[off_y:off_y+h, off_x:off_x+w, :] = img

    if label is not None:
        # label是numpy.ndarray形式
        label = label.copy()
        label[:, :4] += [off_x, off_y, off_x, off_y]
        return dst, label

    return dst 


def random_crop(img, size=(0.8,1), ratio=(0.75, 1.5)):
    p = random.uniform(0, 1)
    if p < 0.5:
        return img

    h, w, c = img.shape

    psize = random.uniform(*size)
    pratio = random.uniform(max(psize**2, ratio[0]), 
                            min(1/psize/psize, ratio[1]))

    pwidth = int(w * psize * np.sqrt(pratio))
    pheight= int(h * psize / np.sqrt(pratio))

    topy = random.randrange(h - pheight)
    topx = random.randrange(w - pwidth)

    return img[topy:topy+pheight, topx:topx+pwidth,:]


def random_crop_det(img, label, size=(0.1,1), ratio=(1/2,2), 
                min_overlaps=(0.1,0.3,0.5,0.7,0.9), max_tmp=30):
    p = random.uniform(0, 1)

    if 0 <= p < 1/3:
        return img, label

    h, w, c = img.shape
    
    for _ in range(max_tmp):
        psize = random.uniform(*size)
        pratio = random.uniform(max(psize**2, ratio[0]), 
                                min(1/psize/psize, ratio[1]))
    
        pwidth = int(w * psize * np.sqrt(pratio))
        pheight= int(h * psize / np.sqrt(pratio))

        topy = random.randrange(h - pheight)
        topx = random.randrange(w - pwidth)

        patch = np.array([topx, topy, topx+pwidth, topy+pheight])

        if 1/3 <= p < 2/3:
            iou = calIOU_np(label[:,:4], patch)
            if iou.min() < random.choice(min_overlaps):
                continue

        centerx = (label[:, 2] + label[:, 0]) / 2
        centery = (label[:, 3] + label[:, 1]) / 2

        maskx = np.logical_and(centerx >= patch[0], centerx <= patch[2])
        masky = np.logical_and(centery >= patch[1], centery <= patch[3])

        mask = np.logical_and(maskx, masky)

        olabel = label[mask]

        if len(olabel) < 1:
            continue

        img = img[patch[1]:patch[3], patch[0]:patch[2],:]
        
        olabel[:, :2] = np.maximum(olabel[:, :2], patch[:2])
        olabel[:, 2:4] = np.minimum(olabel[:, 2:4], patch[2:4])
        olabel[:, :2] -= patch[:2]
        olabel[:, 2:4] -= patch[:2]

        return img, olabel

    return img, label


def resize(img, w, h, label=None, interp=1):
    oh, ow, c = img.shape
    img = mx.image.imresize(img, w, h, interp=interp)

    if label is not None:
        label = label.copy().astype('float')
        label[:,0:3:2] *= w / ow
        label[:,1:4:2] *= h / oh

    return (img, label) if label is not None else img


def flip(img, label=None, px=0, py=0):
    flip_x = np.random.choice([False, True], p=[1-px, px])
    flip_y = np.random.choice([False, True], p=[1-py, py])
    
    h, w, c = img.shape
    if flip_x:
        img = img[:,::-1,:]

        if label is not None:
            x1 = w - label[:,2]
            x2 = w - label[:,0]
    
            label[:,0] = x1
            label[:,2] = x2

    if flip_y:
        img = img[::-1,:,:]

        if label is not None:
            y1 = h - label[:,3]
            y2 = h - label[:,1]
    
            label[:,1] = y1
            label[:,3] = y2

    return (img, label) if label is not None else img


def to_tensor(img):
    if img.ndim == 3:
        return img.transpose((2,0,1)).astype('float32') / 255
    elif img.ndim == 4:
        return img.transpose((0,3,1,2)).astype('float32') / 255


def normalize(img, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
    if img.ndim == 3:
        shape = (3,1,1)
    elif img.ndim == 4:
        shape = (1,3,1,1)

    m = mx.nd.array(mean).reshape(shape)
    s = mx.nd.array(std).reshape(shape)

    img = (img - m) / s

    return img


def color_jitter(img, brightness=50, contrast=0.5, saturation=0.5,
                 hue=18, p=0.5):
    
    img = contrast_brightness(img, c=contrast, b=brightness, p=p)
    img = random_saturation(img, saturation, p=p)
    img = random_hue(img, hue, p=p)
    img = random_gray(img, p=0.8)

    return img
