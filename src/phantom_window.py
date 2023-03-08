from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer
import cv2
from numpy.fft import fft2, fftshift
import numpy as np
from vector import Vector


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
        self.PD_holder.mpl_connect('button_press_event', self.on_press)

        # self.filters_list.activated.connect(self.image_transformation)
        # self.modes_list.activated.connect(self.image_transformation)

        # self.kernal_btn.clicked.connect(self.apply_kernal)
        # self.kernal_spinbox.valueChanged.connect(self.make_kernal)

        # initialization
        self.phantom_img = None
        self.unique_pixels = [0, 24, 255, 49, 101, 77]
        self.tissue_maping = {0: [500, 40], 24: [500, 40], 255: [250, 70], 49: [4000, 2000], 101: [900, 90],
                              77: [900, 90]}
        self.t1_arr = None
        self.t2_arr = None
        self.is_prepared = False

    def load_phantom_image(self, image_path):
        phantom_img = cv2.imread(image_path)
        phantom_img = cv2.cvtColor(phantom_img, cv2.COLOR_BGR2GRAY)
        self.phantom_img = phantom_img
        self.Phantom_holder.draw_image(phantom_img)
        self.prepare_properties(phantom_img)

    def prepare_properties(self, phantom_img):
        self.t1_arr = np.array(phantom_img)
        self.t2_arr = np.array(phantom_img)
        for i in self.unique_pixels:
            self.t1_arr[self.t1_arr == i] = 5000
            self.t2_arr[self.t2_arr == i] = self.tissue_maping[i][1]
        self.is_prepard = True

    def on_press(self, event):
        if self.is_prepard:
            xdata = int(event.xdata)
            ydata = int(event.ydata)
            print("T1 = ", self.t1_arr[xdata, ydata])
            print("T2 = ", self.t2_arr[xdata, ydata])




