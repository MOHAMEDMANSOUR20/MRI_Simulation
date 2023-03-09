from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer


class Sequence_Viewer(qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/sequence_viewer_widget.ui", self)

        self.sequence_holder = Viewer()
        self.sequence_viewer_Layout.addWidget(self.sequence_holder)

