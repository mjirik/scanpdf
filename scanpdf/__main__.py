# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modul is used for GUI of Lisa
"""
import logging
logger = logging.getLogger(__name__)

# import scanpdf.sort
# import sort

from scanpdf import algorithm


mainapp = algorithm.ScanPDF()
mainapp.start_gui()
