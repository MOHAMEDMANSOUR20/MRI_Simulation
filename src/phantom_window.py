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
        self.Phantom_holder.mpl_connect('figure_enter_event', self.on_entry)

        # T1_holder
        self.T1_holder = Viewer()
        self.t1_layout.addWidget(self.T1_holder)
        self.T1_holder.mpl_connect('button_press_event', self.on_press)
        self.T1_holder.mpl_connect('figure_enter_event', self.on_entry)

        # T2_holder
        self.T2_holder = Viewer()
        self.t2_layout.addWidget(self.T2_holder)
        self.T2_holder.mpl_connect('button_press_event', self.on_press)
        self.T2_holder.mpl_connect('figure_enter_event', self.on_entry)

        # PD_holder
        self.PD_holder = Viewer()
        self.pd_layout.addWidget(self.PD_holder)
        self.PD_holder.mpl_connect('figure_enter_event', self.on_entry)
        self.PD_holder.mpl_connect('button_press_event', self.on_press)

        self.pop_wind = Pixel_Info()

        # self.img_qual_comboBox.activated.connect(self.change_size)

        # self.modes_list.activated.connect(self.image_transformation)

        # self.kernal_btn.clicked.connect(self.apply_kernal)
        # self.kernal_spinbox.valueChanged.connect(self.make_kernal)

        # initialization
        self.phantom_img = None
        self.resized_image = None
        self.forcontrast = None
        self.forbrightness = None
        self.PI = math.pi
        self.widgets = [self.Phantom_holder, self.T1_holder, self.T2_holder, self.PD_holder]
        self.image_size = [16, 32, 64]
        self.previous_widget = 0
        self.unique_pixels = [0, 24, 255, 49, 101, 77]
        self.tissue_maping = {0: [500, 40], 24: [500, 40], 255: [250, 70], 49: [4000, 2000], 101: [900, 90],
                              77: [900, 90]}
        self.test_array = np.array(
            [[5, 3, 7],
             [20, 4, 7],
             [6, 8, 2],
             ])
        # self.T2_holder.draw_image(np.abs(np.fft.fft2(self.test_array)))
        self.t1_arr = None
        self.t2_arr = None
        self.is_prepared = False

    def draw_phantom_image(self, phantom_img, resized):
        self.phantom_img = phantom_img
        self.resized_image = resized
        self.forcontrast = self.resized_image.copy()
        self.forbrightness = self.resized_image.copy()
        self.phantom_tabWidget.setCurrentIndex(0)
        self.Phantom_holder.clear_canvans()
        self.Phantom_holder.draw_image(resized)
        Reconstruction.store_slice(resized)
        self.prepare_properties(resized)

    def prepare_properties(self, phantom_img):
        self.t1_arr = np.array(phantom_img).astype(np.int16)
        self.t2_arr = np.array(phantom_img).astype(np.int16)
        self.pd_arr = np.ones(self.t2_arr.shape)
        for i in self.unique_pixels:
            self.t1_arr[self.t1_arr == i] = self.tissue_maping[i][0]
            self.t2_arr[self.t2_arr == i] = self.tissue_maping[i][1]

        self.T1_holder.draw_image(self.t1_arr)
        self.T2_holder.draw_image(self.t2_arr)
        self.PD_holder.draw_image(self.pd_arr, vmax=1, vmin=0)
        self.is_prepard = True

        # self.apply_sequence(self.test_array)

    def on_press(self, event):
        try:
            self.pop_wind.close()
            xdata = event.xdata - 0.5
            ydata = event.ydata - 0.5
            size = self.image_size[self.img_qual_comboBox.currentIndex()]
            self.widgets[self.previous_widget].remove_rectangle()

            self.widgets[self.phantom_tabWidget.currentIndex()].show_rectangle(xdata,
                                                                               ydata, 1, 1)

            self.pop_wind.show_properties(
                [int(xdata), int(ydata), self.t1_arr[int(ydata), int(xdata)], self.t2_arr[int(ydata), int(xdata)],
                 self.pd_arr[int(ydata), int(xdata)]])

            self.previous_widget = self.phantom_tabWidget.currentIndex()
        except:
            pass

    def on_entry(self, event):
        try:
            if not self.pop_wind.isVisible():
                self.widgets[self.phantom_tabWidget.currentIndex()].remove_rectangle()
        except:
            pass

    def change_size(self):
        try:
            size = self.image_size[self.img_qual_comboBox.currentIndex()]
            resized_img = cv2.resize(self.phantom_img, (size, size))
            self.draw_phantom_image(self.phantom_img, resized_img)

        except:
            pass

    def change_brightness(self, value):
        try:
            brightness = int(255 * value / 100)
            img = (self.forbrightness.astype(np.int16).copy() + brightness)
            self.forcontrast =img
            self.Phantom_holder.draw_image(img, 0, 255)
        except:
            pass

    def change_contrast(self, value):
        try:
            alpha = (100.0 + value) / 100.0
            # compute new image pixel values based on alpha
            min_val, max_val = np.min(self.forcontrast), np.max(self.forcontrast)
            avg_val = (max_val + min_val) / 2.0
            image = (self.forcontrast.astype(np.int16).copy() - avg_val) * alpha + avg_val
            self.forbrightness = image
            self.Phantom_holder.draw_image(image, 0, 255)

        except:
            pass
