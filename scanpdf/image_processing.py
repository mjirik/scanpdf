# /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import sys
import glob
import os.path as op
import os
import shutil
import numpy as np
from matplotlib import pyplot as plt
import scipy.misc
import skimage.transform
import skimage.io
import scanpdf.deskew

def skip_empty(processing_params):
    empty_pages = 0
    for i, ppars in enumerate(processing_params):
        im = plt.imread(ppars["fn"])
        img = skimage.color.rgb2gray(im)
        black_pixels = np.sum(img < 0.9) / np.prod(img.shape)
        if black_pixels < 0.005:
            # empty page
            processing_params.pop(i)
            print("empty page ", ppars["fn"])
            empty_pages += 1
        else:
            # normal page
            ppars["inew"] = ppars["inew"] - empty_pages
    return processing_params


def angle_measurement(processing_params):
    for i, ppars in enumerate(processing_params):
        im = skimage.io.imread(ppars["fn"])
        imgr = skimage.color.rgb2gray(im)
        # imrot = (skimage.transform.rotate(imgr, 3, cval=0.98) * 255).astype(np.uint8)
        imres = (skimage.transform.resize(imgr, (3504, 2480)) * 255).astype(np.uint8)
        angle1 = scanpdf.deskew.deskew_determ(imres)
        ppars["angle"] = angle1
    return processing_params

