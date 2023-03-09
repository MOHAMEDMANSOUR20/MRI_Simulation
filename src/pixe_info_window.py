from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import sys

class Pixel_Info(qtw.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/pixel_info_window.ui")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    win = Pixel_Info()
    win.show()
    sys.exit(app.exec_())