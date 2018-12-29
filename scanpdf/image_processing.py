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


def skip_empty(processing_params, margin_percent=5, black_threshold=0.85, pixel_number_threshold=0.002):
    empty_pages = 0
    for i, ppars in enumerate(processing_params):
        im = plt.imread(ppars["fn"])
        img = skimage.color.rgb2gray(im)

        margin = ((0.01 * margin_percent) * np.asarray(img.shape)).astype(np.int)
        img = img[
              margin[0]:-margin[0],
              margin[1]:-margin[1]
              ]
        black_pixels = np.sum(img < black_threshold) / np.prod(img.shape)
        dbg_inew = ppars["inew"]
        if black_pixels < pixel_number_threshold:
            # empty page
            # processing_params.pop(i)
            ppars["empty"] = True
            #print("empty page ", ppars["fn"])
            empty_pages += 1
        else:
            # normal page
            ppars["inew"] = ppars["inew"] - empty_pages
            ppars["empty"] = False
        logger.debug("skip empty {} {} {} {} {}".format(
            ppars["empty"], i, dbg_inew, ppars["inew"], ppars["fn"][-10:]))
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

