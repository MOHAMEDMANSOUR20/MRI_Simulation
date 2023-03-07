from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import mediapipe as mp
import sys
import qdarkstyle
from PyQt5.QtCore import pyqtSlot
from phantom_window import PhantomWindow


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("src/ui/mainWindow.ui", self)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.phantom_window = PhantomWindow()
        self.centralWidget().layout().addWidget(self.phantom_window)
        self.browse_action.triggered.connect(self.Load_phantom_file)

    @pyqtSlot()
    def Load_phantom_file(self):
        image_path = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.phantom_window.load_phantom_image(image_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
