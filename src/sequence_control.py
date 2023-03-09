from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer

class Sequence_Controller(qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/sequence_control_widget.ui", self)



