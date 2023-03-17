import sys

import qdarkstyle
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from PyQt5 import QtCore

from viewer import Viewer


class Pixel_Info(qtw.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/pixel_info_window.ui", self)
        #self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        #self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def show_properties(self, info_list):
        self.x_info_label.setText(str(info_list[0]))
        self.y_info_label.setText(str(info_list[1]))
        self.t1_info_label.setText(str(info_list[2]))
        self.t2_info_label.setText(str(info_list[3]))
        self.proton_density_info_label.setText(str(info_list[4]))
        self.show()



    #
    # def focusInEvent(self, event):
    #     super().focusInEvent(event)
    #     self.clearFocus()
