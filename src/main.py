from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer
import sys
import qdarkstyle
from PyQt5.QtCore import pyqtSlot
from phantom_window import PhantomWindow
from reconstruction_window import Reconstruction
from sequence_viewer import Sequence_Viewer
from sequence_controller import Sequence_Controller
from pixe_info_window import Pixel_Info


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/MRI_Simulator_GUI.ui", self)

        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.phantom_window = PhantomWindow()
        self.reconstruction_window = Reconstruction()
        self.sequence_controller = Sequence_Controller()
        self.sequence_control_Layout.addWidget(self.sequence_controller)
        self.phantom_img_Layout.addWidget(self.phantom_window)
        self.reconstruction_Layout.addWidget(self.reconstruction_window)
        self.sequence_viewer = Sequence_Viewer()
        self.sequence_viewer_Layout.addWidget(self.sequence_viewer)
        # self.sequence_Layout.addWidget(self.sequence_holder)

        # Actions
        self.sequence_controller.Simulate_Button.clicked.connect(self.reconstruction_window.apply_sequence)
        self.action_Phantom.triggered.connect(self.Load_phantom_file)
        self.action_Sequence.triggered.connect(self.Load_sequence_file)

        # Just for trying pop out window
        # self.sequence_controller.export_Button.clicked.connect(self.pop_wind.show)
        # self.sequence_controller.Simulate_Button.clicked.connect(self.pop_wind.close)


    @pyqtSlot()
    def Load_phantom_file(self):
        image_path = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.phantom_window.load_phantom_image(image_path)

    @pyqtSlot()
    def Load_sequence_file(self):
        image_path = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
