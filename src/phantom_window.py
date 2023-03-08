import math
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from viewer import Viewer
import cv2
from numpy.fft import fft2, fftshift
import numpy as np
from vector import Vector
from rotation import Rotation


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
        self.Rotation_matrix = Rotation()

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
        self.T2_holder.draw_image(np.abs(np.fft.fft2(self.test_array)))
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
        self.apply_sequence(self.test_array)

    def apply_sequence(self, phantom_img):
        num_row = phantom_img.shape[0]
        num_column = phantom_img.shape[1]
        img_vectors = np.ones((num_row, num_column, 3))
        img_vectors[:, :, 2] = img_vectors[:, :, 2] * phantom_img
        img_vectors[:, :, 0] = 0
        img_vectors[:, :, 1] = 0
        R_forRF = self.Rotation_matrix.RX(self.PI / 2).T
        img_vectors = np.matmul(img_vectors[:], R_forRF)
        print(img_vectors[0, 0, 1], R_forRF)

        step_inGY = 2 * self.PI / num_row
        step_inGx = 2 * self.PI / num_column
        img_vector_changed = img_vectors
        vector_summation = []
        for i in range(num_row):
            step_y_inner = (step_inGY * (i+1))/num_row
            vector_sum = []
            for i_inner in range(num_row):
                R_forGY = self.Rotation_matrix.RZ(step_y_inner * i_inner).T
                img_vector_changed[i_inner, :, :] = np.matmul(img_vector_changed[i_inner, :, :], R_forGY)
            for j in range(num_column):
                R_forGX = self.Rotation_matrix.RZ(step_inGx * j).T
                img_vector_changed[:, j, :] = np.matmul(img_vector_changed[:, j, :], R_forGX)

                x_sum = np.sum(img_vector_changed[:, :, 0])
                y_sum = np.sum(img_vector_changed[:, :, 1])
                s_spin = np.sqrt(x_sum ** 2 + y_sum ** 2)
                vector_sum.append(s_spin)
            vector_summation.append(vector_sum)
            img_vector_changed = img_vectors
        # F1Mag_F2Phase = np.abs(np.fft.ifft(vector_summation))
        self.T1_holder.draw_image(vector_summation)

    def on_press(self, event):
        if self.is_prepard:
            xdata = int(event.xdata)
            ydata = int(event.ydata)
            print("T1 = ", self.t1_arr[xdata, ydata])
            print("T2 = ", self.t2_arr[xdata, ydata])
