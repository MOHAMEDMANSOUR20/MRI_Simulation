from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer
import cv2


class Reconstruction(qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/reconstruction_widget.ui", self)

        self.Reconstruction_holder = Viewer()
        self.Reconstruction_Layout.addWidget(self.Reconstruction_holder)
        self.K_Space_holder = Viewer()
        self.K_Space_Layout.addWidget(self.K_Space_holder)
