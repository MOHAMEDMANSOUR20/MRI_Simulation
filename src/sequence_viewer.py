from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer, Sequence_Drawer
from sequence_controller import Sequence_Controller
import math


class Sequence_Viewer(qtw.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/sequence_viewer_widget.ui", self)
        self.img_shape = [0,0]
        self.sequence_controller = Sequence_Controller()
        self.sequence_control_Layout.addWidget(self.sequence_controller)

        self.sequence_holder = Sequence_Drawer()
        self.sequence_viewer_Layout.addWidget(self.sequence_holder)

        self.sequence_controller.RF_Slider.valueChanged.connect(self.get_rf_value)
        self.sequence_controller.Slice_Selection_Slider.valueChanged.connect(self.get_slice_selection_value)
        self.sequence_controller.Gy_Slider.valueChanged.connect(self.get_Gy_value)
        self.sequence_controller.Gx_Slider.valueChanged.connect(self.get_Gx_value)
        self.sequence_controller.te_Slider.valueChanged.connect(self.get_TE_value)
        self.sequence_controller.tr_Slider.valueChanged.connect(self.get_TR_value)

    def get_rf_value(self):
        rf = self.sequence_controller.RF_Slider.value()
        tr = self.sequence_controller.tr_Slider.value()
        self.sequence_controller.json_file.data["Sequence"]["RF"] = rf
        rf = rf / 1000
        self.sequence_holder.draw_rf(rf, tr)

    def get_slice_selection_value(self):
        slice = self.sequence_controller.Slice_Selection_Slider.value()
        self.sequence_controller.json_file.data["Sequence"]["Slice"] = slice
        slice = slice / 1000
        self.sequence_holder.draw_slice_selection(slice)


    def get_Gy_value(self):
        gy = self.sequence_controller.Gy_Slider.value()
        tr = self.sequence_controller.tr_Slider.value()
        self.sequence_controller.json_file.data["Sequence"]["GY"] = gy
        gy = tr * gy / 1000
        img_rows = self.img_shape[0]
        if img_rows > 0:
            self.sequence_holder.draw_gy(img_rows, gy)


    def get_Gx_value(self):
        gx = self.sequence_controller.Gx_Slider.value()
        tr = self.sequence_controller.tr_Slider.value()
        self.sequence_controller.json_file.data["Sequence"]["GX"] = gx
        te = self.sequence_controller.te_Slider.value() * tr / 1000

        gx = gx / 1000
        self.sequence_holder.draw_gx(te, gx)

    def get_TE_value(self):
        te = self.sequence_controller.te_Slider.value()
        tr = self.sequence_controller.tr_Slider.value()
        self.sequence_controller.json_file.data["Sequence"]["TE"] = te
        te = tr * te/1000
        self.sequence_controller.te_val_label.setText(f"{te} ms")
        gx = self.sequence_controller.Gx_Slider.value() / 1000
        self.sequence_holder.draw_gx(te, gx)

        self.sequence_holder.draw_read_signal(te)


    def get_TR_value(self):
        tr = self.sequence_controller.tr_Slider.value()
        self.sequence_controller.json_file.data["Sequence"]["TR"] = tr
        self.sequence_controller.tr_val_label.setText(f"{tr} ms")
        self.sequence_holder.set_tr(tr)
        self.get_TE_value()
        self.get_Gy_value()


