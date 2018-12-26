# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modul is used for GUI of Lisa
"""
import logging
logger = logging.getLogger(__name__)

# import scanpdf.sort
# import sort
print("ahoj")

from scanpdf import algorithm


print("gui before start")
mainapp = algorithm.ScanPDF()
print("gui started")
mainapp.start_gui()
print("gui started")