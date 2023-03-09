import math
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic

from src.pixe_info_window import Pixel_Info
from viewer import Viewer
import cv2
import numpy as np
from reconstruction_window import Reconstruction


class PhantomWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.is_prepard = False
        uic.loadUi("ui/phantom_widget.ui", self)

        # Phantom_holder
        self.Phantom_holder = Viewer()
        self.phantom_layout.addWidget(self.Phantom_holder)
        self.Phantom_holder.mpl_connect('button_press_event', self.on_press)
        # T1_holder
        self.T1_holder = Viewer()
        self.t1_layout.addWidget(self.T1_holder)
        self.T1_holder.mpl_connect('button_press_event', self.on_press)
        # T2_holder
        self.T2_holder = Viewer()
        self.t2_layout.addWidget(self.T2_holder)
        self.T2_holder.mpl_connect('button_press_event', self.on_press)
        # PD_holder
        self.PD_holder = Viewer()
        self.pd_layout.addWidget(self.PD_holder)
        self.pop_wind = Pixel_Info()

        # self.PD_holder.mpl_connect('button_press_event', self.on_press)

        # self.filters_list.activated.connect(self.image_transformation)
        # self.modes_list.activated.connect(self.image_transformation)

        # self.kernal_btn.clicked.connect(self.apply_kernal)
        # self.kernal_spinbox.valueChanged.connect(self.make_kernal)

        # initialization
        self.phantom_img = None
        self.PI = math.pi
        self.unique_pixels = [0, 24, 255, 49, 101, 77]
        self.tissue_maping = {0: [500, 40], 24: [500, 40], 255: [250, 70], 49: [4000, 2000], 101: [900, 90],
                              77: [900, 90]}
        self.test_array = np.array(
            [[2, 3, 5],
             [5, 10, 7],
             [1, 8, 2]])
        # self.T2_holder.draw_image(np.abs(np.fft.fft2(self.test_array)))
        self.t1_arr = None
        self.t2_arr = None
        self.is_prepared = False

    def load_phantom_image(self, image_path):
        phantom_img = cv2.imread(image_path)
        phantom_img = cv2.cvtColor(phantom_img, cv2.COLOR_BGR2GRAY)
        self.phantom_img = phantom_img
        self.Phantom_holder.draw_image(phantom_img)
        Reconstruction.store_slice(self.test_array)
        self.prepare_properties(phantom_img)

    def prepare_properties(self, phantom_img):
        self.t1_arr = np.array(phantom_img).astype(np.int16)
        self.t2_arr = np.array(phantom_img).astype(np.int16)
        self.pd_arr = np.ones(self.t2_arr.shape)
        for i in self.unique_pixels:
            self.t1_arr[self.t1_arr == i] = self.tissue_maping[i][0]
            self.t2_arr[self.t2_arr == i] = self.tissue_maping[i][1]
        self.is_prepard = True
        self.T1_holder.draw_image(self.t1_arr)
        self.T2_holder.draw_image(self.t2_arr)
        self.PD_holder.draw_image(self.pd_arr, vmax=1, vmin=0)

        # self.apply_sequence(self.test_array)

    def on_press(self, event):
        if self.is_prepard:
            xdata = int(event.xdata)
            ydata = int(event.ydata)
            self.pop_wind.show_properties(
                [xdata, ydata, self.t1_arr[ydata, xdata], self.t2_arr[ydata, xdata], self.pd_arr[ydata, xdata]])
            self.pop_wind.show()

