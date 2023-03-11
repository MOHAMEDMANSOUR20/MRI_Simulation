from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer
import sys
import qdarkstyle
from PyQt5.QtCore import pyqtSlot
from phantom_window import PhantomWindow
from reconstruction_window import Reconstruction
from sequence_viewer import Sequence_Viewer

from sequence_data import Sequence_Data
from pixe_info_window import Pixel_Info


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/MRI_Simulator_GUI.ui", self)

        #self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        #self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.phantom_window = PhantomWindow()
        self.reconstruction_window = Reconstruction()
        self.phantom_img_Layout.addWidget(self.phantom_window)
        self.reconstruction_Layout.addWidget(self.reconstruction_window)
        self.sequence_viewer = Sequence_Viewer()
        self.sequence_Layout.addWidget(self.sequence_viewer)


        # Actions
        self.sequence_viewer.sequence_controller.Simulate_Button.clicked.connect(self.reconstruction_window.apply_sequence)
        self.action_Phantom.triggered.connect(self.Load_phantom_file)
        self.action_Sequence.triggered.connect(self.Load_sequence_file)

        # Just for trying pop out window
        # self.sequence_controller.export_Button.clicked.connect(self.pop_wind.show)
        # self.sequence_controller.Simulate_Button.clicked.connect(self.pop_wind.close)


    @pyqtSlot()
    def Load_phantom_file(self):
        image_path = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.phantom_window.load_phantom_image(image_path)
        self.reconstruction_window.Reconstruction_holder.clear_canvans()
        self.reconstruction_window.K_Space_holder.clear_canvans()


    @pyqtSlot()
    def Load_sequence_file(self):
        file_path = qtw.QFileDialog.getOpenFileName(filter="Text files (*.json)")[0]
        self.sequence_viewer.sequence_controller.json_file.read_json(file_path)
        rf = self.sequence_viewer.sequence_controller.json_file.data["Sequence"]["RF"]# / 1000
        slice = self.sequence_viewer.sequence_controller.json_file.data["Sequence"]["Slice"] #
        gy = self.sequence_viewer.sequence_controller.json_file.data["Sequence"]["GY"] #* (2/1000)
        gx = self.sequence_viewer.sequence_controller.json_file.data["Sequence"]["GX"] #* (2/1000)
        te = self.sequence_viewer.sequence_controller.json_file.data["Sequence"]["TE"]
        tr = self.sequence_viewer.sequence_controller.json_file.data["Sequence"]["TR"]

        self.sequence_viewer.sequence_controller.RF_Slider.setValue(rf)
        self.sequence_viewer.sequence_controller.Slice_Selection_Slider.setValue(slice)
        self.sequence_viewer.sequence_controller.Gy_Slider.setValue(gy)
        self.sequence_viewer.sequence_controller.Gx_Slider.setValue(gx)
        self.sequence_viewer.sequence_controller.te_Slider.setValue(te)
        self.sequence_viewer.sequence_controller.tr_Slider.setValue(tr)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
