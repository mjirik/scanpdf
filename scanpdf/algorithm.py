# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modul is used for GUI of Lisa
"""
import logging
logger = logging.getLogger(__name__)

import sys
import os.path as op
# import PyQt5
# import PyQt5.QtWidgets
print("start 3")
# from PyQt5.QtWidgets import QApplication, QFileDialog
# print("start 4")
print("start 4")
import pyqtgraph as pg
import glob
from pyqtgraph.parametertree import Parameter, ParameterTree
from PIL import Image
import ruamel.yaml

# from scaffan import image
# import io3d
# import io3d.datasets
# import scaffan.lobulus
# import scaffan.report
import scanpdf.sort
import scanpdf.image_processing


class ScanPDF:

    def __init__(self):
        params = [
            {"name": "Input", "type": "group", "children": [
                {'name': 'Dir Path', 'type': 'str', "value": self._prepare_default_input_dir()},
                {'name': 'Select', 'type': 'action'},
            ], },

            {"name": "Sort", "type": "group", "children": [
                {'name': 'Reverse odd pages', 'type': 'bool', 'value': False , 'tip': "Show images"},
                {'name': 'Reverse even pages', 'type': 'bool', 'value': True, 'tip': "Show images"},
                {'name': 'Turn odd pages', 'type': 'bool', 'value': False, 'tip': "Show images"},
                {'name': 'Turn even pages', 'type': 'bool', 'value': True, 'tip': "Show images"},
            ], },
            {"name": "Image processing", "type": "group", "children": [
                {'name': 'Skip empty pages', 'type': 'bool', 'value': True, 'tip': "Show images"},
                {'name': 'Fix orientation', 'type': 'bool', 'value': True, 'tip': "Show images"},
                # {'name': 'Turn odd pages', 'type': 'bool', 'value': True, 'tip': "Show images"},
                # {'name': 'Turn even pages', 'type': 'bool', 'value': False, 'tip': "Show images"},
            ], },
            {'name': 'Make dir with image files', 'type': 'action'},
                # {'name': 'Annotation Color', 'type': 'list', 'values': {
                #     "None": None,
                #     "White": "#FFFFFF",
                #     "Black": "#000000",
                #     "Red": "#FF0000",
                #     "Green": "#00FF00",
                #     "Blue": "#0000FF",
                #     "Cyan": "#00FFFF",
                #     "Magenta": "#FF00FF",
                #     "Yellow": "#FFFF00"},
                #  'value': 0},
                # {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
                # {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
            # {"name": "Output", "type": "group", "children": [
            #     {'name': 'Directory Path', 'type': 'str', 'value': self._prepare_default_output_dir()},
            #     {'name': 'Select', 'type': 'action'},
            # ], },
            {"name": "Make PDF", "type": "group", "children": [
                {'name': 'Split file names', 'type': 'text', 'value': '1: Default', "tip": "Line format\n[Page number]: [File name without pdf extension]"},
                {'name': "Auto split suggestion", 'type': 'action'},
                {'name': 'Skip empty pages', 'type': 'bool', 'value': True, 'tip': "Show images"},
                {'name': 'Fix orientation', 'type': 'bool', 'value': True, 'tip': "Show images"},
                # {'name': 'Turn odd pages', 'type': 'bool', 'value': True, 'tip': "Show images"},
                # {'name': 'Turn even pages', 'type': 'bool', 'value': False, 'tip': "Show images"},
            ], },
            {'name': "Make PDF's", 'type': 'action'},
            # {"name": "Processing", "type": "group", "children": [
            #     # {'name': 'Directory Path', 'type': 'str', 'value': prepare_default_output_dir()},
            #     {'name': 'Run', 'type': 'action'},
            #     {'name': 'Show', 'type': 'bool', 'value': False , 'tip': "Show images"},
            # ], }
        ]
        self.parameters = Parameter.create(name='params', type='group', children=params)
        self.anim = None

    def auto_split_file_names(self):
        import tesserocr
        import re
        path = self.parameters.param("Input", "Dir Path").value()
        head, teil = op.split(path)
        jpgs_path = op.join(head, teil + " - sorted")
        fns = glob.glob(op.join(jpgs_path, "*"))
        # im = skimage.io.imread(fns[0])
        data = {}
        for i, fn in enumerate(fns):
            im = Image.open(fn)
            w, h = im.size
            imcr = im.crop((0, 30, w, int(0.10 * h)))
            im.close()
            text = tesserocr.image_to_text(imcr)
            text = text.strip()
            text = re.sub('"', '', text)
            text = re.sub(r"['‘’?§;,>“—-]:", '', text)
            text = re.sub(r"\s+", ' ', text)
            #     text = re.sub(r"^\s*\n", '', text)
            #     text = re.sub(' +', ' ', text)
            #     text = re.sub(r'\n\s*\n', r'\n', text)
            text = re.sub(r'^\s*\d+[\s\d]*$', '', text)

            text = text.strip()
            if len(text) > 0:
                print(i + 1, ":", text)
                data[i + 1] = text

        yaml_text = ruamel.yaml.round_trip_dump(data)
        path = self.parameters.param("Make PDF", "Split file names").setValue(yaml_text)





    # def select_file_gui(self):
    #     from PyQt5 import QtWidgets
    #     # default_dir = io3d.datasets.join_path(get_root=True)
    #     # default_dir = op.expanduser("~/data")
    #     # if not op.exists(default_dir):
    #     # default_dir = op.expanduser("~")
    #     fnparam = self.parameters.param("Input", "Dir Path")
    #     default_dir = fnparam.value()
    #
    #     fn, mask = QtWidgets.QFileDialog.getOpenFileName(
    #         None, "Select Input File", directory=default_dir,
    #         filter="NanoZoomer Digital Pathology Image(*.ndpi)"
    #     )
    #     self.set_input_dir(fn)

    def set_input_dir(self, fn):
        fnparam = self.parameters.param("Input", "Dir Path")
        fnparam.setValue(fn)
        # import pdb; pdb.set_trace()
        # print("ahoj")

    # def set_output_dir(self, path):
    #     fnparam = self.parameters.param("Output", "Directory Path")
    #     fnparam.setValue(path)

    def select_input_dir_gui(self):
        from PyQt5 import QtWidgets
        default_dir = self._prepare_default_input_dir()

        fn = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select Output Directory", directory=default_dir,
            # filter="NanoZoomer Digital Pathology Image(*.ndpi)"
        )
        # print (fn)
        self.set_input_dir(fn)


    def _prepare_default_input_dir(self):
        # default_dir = io3d.datasets.join_path(get_root=True)
        default_dir = op.expanduser("~/Documents/Scanned Documents/")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~/Documents/")
            if not op.exists(default_dir):
                default_dir = op.expanduser("~")
        return default_dir

    def init_run(self):
        fnparam = self.parameters.param("Input", "File Path")
        path = fnparam.value()
        # self.anim = image.AnnotatedImage(path)
        # fnparam = self.parameters.param("Output", "Directory Path")
        # self.report = scaffan.report.Report(fnparam.value())

    def make_dir_with_files(self):
        path = self.parameters.param("Input", "Dir Path").value()
        self.output_dir = scanpdf.sort.make_output_dir(path)
        processing_params = scanpdf.sort.sort_prepare_parameters(
            path,
            reverse_odd_pages=self.parameters.param("Sort", "Reverse odd pages").value(),
            reverse_even_pages=self.parameters.param("Sort", "Reverse even pages").value(),
            turn_odd_pages=self.parameters.param("Sort", "Turn odd pages").value(),
            turn_even_pages=self.parameters.param("Sort", "Turn even pages").value(),
        )
        if self.parameters.param("Image processing", "Skip empty pages").value():
            processing_params = scanpdf.image_processing.skip_empty(processing_params)
        if self.parameters.param("Image processing", "Fix orientation").value():
            processing_params = scanpdf.image_processing.angle_measurement(processing_params)

        scanpdf.sort.sort_write_output(processing_params, output_path=self.output_dir)

    def make_pdfs(self):
        path = self.parameters.param("Input", "Dir Path").value()
        self.output_dir = scanpdf.sort.make_output_dir(path)
        pdf_filename = self.parameters.param("Input", "Dir Path").value() + ".pdf"
        # fns = glob.glob(op.join(jpgs_path, "*"))
        types = ('*.png', '*.jpg', "*.jpeg", "*.bmp")  # the tuple of file types
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(op.join(self.output_dir, files)))
        files_grabbed  # the list of pdf and cpp files
        fns = files_grabbed
        yaml_text = self.parameters.param("Make PDF", "Split file names").value()
        data = ruamel.yaml.load(yaml_text)
        print(data)
        im_list = []
        for fn in fns:
            im = Image.open(fn)
            im_list.append(im)

        im0 = im_list.pop(0)
        im0.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)


    # def set_annotation_color_selection(self, color):
    #     pcolor = self.parameters.param("Input", "Annotation Color")
    #     color = color.upper()
    #     if color in pcolor.reverse[0]:
    #         # val = pcolor.reverse[0].index(color)
    #         # pcolor.setValue(val)
    #         pcolor.setValue(color)
    #     else:
    #         raise ValueError("Color '{}' not found in allowed colors.".format(color))

    #
    #
    # def run_lobuluses(self, color=None):
    #     self.init_run()
    #     pcolor = self.parameters.param("Input", "Annotation Color")
    #     print("color ", pcolor.value())
    #     # color = pcolor.reverse[0][pcolor.value()]
    #     color = pcolor.value()
    #     # print("Color ", color)
    #     # fnparam = self.parameters.param("Input", "File Path")
    #     # from .image import AnnotatedImage
    #     # path = self.parameters.param("Input", "File Path")
    #     # anim = AnnotatedImage(path.value())
    #     # if color is None:
    #     #     color = list(self.anim.colors.keys())[0]
    #     # print(self.anim.colors)
    #     annotation_ids = self.anim.select_annotations_by_color(color)
    #     logger.debug("Annotation IDs: {}".format(annotation_ids))
    #     for id in annotation_ids:
    #         self._run_lobulus(id)
    #     self.report.df.to_excel(op.join(self.report.outputdir, "data.xlsx"))
    #
    #     # print("ann ids", annotation_ids)
    # def _run_lobulus(self, annotation_id):
    #     show = self.parameters.param("Processing", "Show").value()
    #     lobulus = scaffan.lobulus.Lobulus(self.anim, annotation_id, report=self.report)
    #     lobulus.find_border(show=show)
    #     pass


    def start_gui(self):

        from PyQt5 import QtGui
        from PyQt5 import QtWidgets
        # import QApplication, QFileDialog
        app = QtWidgets.QApplication(sys.argv)


        self.parameters.param('Input', 'Select').sigActivated.connect(self.select_input_dir_gui)
        self.parameters.param('Make dir with image files').sigActivated.connect(self.make_dir_with_files)
        self.parameters.param("Make PDF's").sigActivated.connect(self.make_pdfs)
        self.parameters.param("Make PDF", "Auto split suggestion").sigActivated.connect(self.auto_split_file_names)

        t = ParameterTree()
        t.setParameters(self.parameters, showTop=False)
        t.setWindowTitle('pyqtgraph example: Parameter Tree')
        # t.show()


        print("run scaffan")
        win = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        win.setLayout(layout)
        # layout.addWidget(QtGui.QLabel("These are two views of the same data. They should always display the same values."), 0,  0, 1, 2)
        layout.addWidget(t, 1, 0, 1, 1)
        # layout.addWidget(t2, 1, 1, 1, 1)
        win.show()
        win.resize(800, 800)

        app.exec_()


