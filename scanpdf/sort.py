# /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)
# conda create -c conda-forge -n -c mcs07 scanpdf python=3.6 numpy scikit-image jupyter tesseract

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

def make_output_dir(path):
    head, teil = op.split(path)
    output_path = op.join(head, teil + " - sorted")
    if not op.exists(output_path):
        import os
        os.makedirs(output_path)
    return output_path


def sort_prepare_parameters(path, reverse_odd_pages=False, reverse_even_pages=True, turn_odd_pages=False, turn_even_pages=True):
    fns = glob.glob(op.join(path, "*"))
    fns.sort(key=os.path.getmtime)

    length = len(fns)
    if length % 2 == 1:
        raise ValueError("Even number of files expected")
    len2 = int(length / 2)

    processing_params = [None] * length
    # fns sorted by datetime
    for i, fn in enumerate(fns):
        turn = False
        if i < len2:
            # odd
            if reverse_odd_pages:
                inew = ((len2 - i) * 2) + 1
            else:
                inew = (i * 2) + 1
            turn = turn_odd_pages
        else:
            # even
            if reverse_even_pages:
                inew = (length - i) * 2
            else:
                inew = (i - len2) * 2
            turn = turn_even_pages

        processing_params[inew - 1] = {"inew": inew, "turn": turn, "fn": fn}
        print(inew, turn, fn)
    return processing_params


def sort_write_output(processing_params, output_path):
    for ppars in processing_params:
        inew = ppars["inew"]
        turn = ppars["turn"]
        fn = ppars["fn"]
        _, ext = op.splitext(fn)

         # = processing_params[i]
        new_short_fn = '{:04d}'.format(inew) + ext
        print(new_short_fn, inew, ppars["empty"], fn[-10:])
        if ppars["empty"]:
            new_short_fn = "empty_" + new_short_fn
            # continue
        new_fn = op.join(output_path, new_short_fn)
        im = skimage.io.imread(fn)
        if turn:
            im = skimage.transform.rotate(im, 180)
        if "angle" in ppars:
            im = skimage.transform.rotate(im, ppars["angle"], cval=1)

        skimage.io.imsave(new_fn, im)


