import math
from PyQt5 import QtWidgets as qtw, QtWidgets
from PyQt5 import uic
from src.rotation import Rotation
from src.sequence_data import Sequence_Data
from viewer import Viewer
import numpy as np


class Reconstruction(qtw.QWidget):
    image_opened = False
    test_image = None
    sequence_prepared = True
    forcontrast = None
    forbrightness = None
    completed = False
    sequence = {}

    def __init__(self):
        super().__init__()

        uic.loadUi("ui/reconstruction_widget.ui", self)
        self.Reconstruction_holder = Viewer()
        self.Reconstruction_Layout.addWidget(self.Reconstruction_holder)
        self.K_Space_holder = Viewer()
        self.K_Space_Layout.addWidget(self.K_Space_holder)
        self.Rotation_matrix = Rotation()
        self.PI = math.pi

    def apply_sequence(self):
        if Reconstruction.is_prepared():
            Reconstruction.completed = False
            self.Reconstruction_holder.clear_canvans()
            self.K_Space_holder.clear_canvans()
            phantom_img = Reconstruction.test_image
            num_row = phantom_img.shape[0]
            num_column = phantom_img.shape[1]
            img_vectors = np.ones((num_row, num_column, 3))
            img_vectors[:, :, 2] = phantom_img
            img_vectors[:, :, 0] = 0
            img_vectors[:, :, 1] = 0
            step_inGY = 2 * self.PI / num_row
            step_inGx = 2 * self.PI / num_column
            vector_sum = np.empty(num_column, dtype=complex)
            vector_summation = np.zeros((num_row, num_column), dtype=complex)
            for i in range(num_row):
                R_forRF = self.Rotation_matrix.RY(self.PI / 2).T
                img_vector_changed = np.matmul(img_vectors, R_forRF)
                for i_inner in range(num_row):
                    R_forGY = self.Rotation_matrix.RZ(i_inner * step_inGY * i).T
                    img_vector_changed[i_inner, :, :] = \
                        np.matmul(img_vector_changed[i_inner, :, :], R_forGY)
                for j in range(num_column):
                    img_vector_changed_x = img_vector_changed.copy()
                    for j_inner in range(num_column):
                        R_forGX = self.Rotation_matrix.RZ(step_inGx * j_inner * j).T
                        img_vector_changed_x[:, j_inner, :] = \
                            np.matmul(img_vector_changed_x[:, j_inner, :], R_forGX)
                    x_sum = np.sum(img_vector_changed_x[:, :, 0])
                    y_sum = np.sum(img_vector_changed_x[:, :, 1])
                    vector_sum[-j] = np.complex(x_sum, y_sum)

                vector_summation[-i] = vector_sum
                self.K_Space_holder.draw_image(np.abs(np.fft.fftshift(vector_summation)), animate=True)
                self.Reconstruction_holder.draw_image(np.abs(np.fft.ifft2(vector_summation)), animate=True)
            Reconstruction.completed = True
            # img_vector_changed = np.matmul(img_vector_changed, -1 * R_forRF)

            # print((np.fft.fftshift(vector_summation)))
            # print(np.fft.fftshift(np.fft.fft2(Reconstruction.test_image)))
            # reconstruced_slice = np.abs(np.fft.ifft2(np.fft.ifftshift(vector_summation)))
            # self.K_Space_holder.draw_image(np.abs(np.fft.fftshift(vector_summation)))
            # self.Reconstruction_holder.draw_image(np.abs(np.fft.ifft2(vector_summation)))

        else:
            QtWidgets.QMessageBox.about(
                self, "Error", "Open phantom first")

    def change_brightness(self, value):
        try:
            self.bright_val_label.setText(str(self.brightness_Slider.value()) + " %")
            if Reconstruction.completed:
                brightness = int(250 * value / 100)
                img = (Reconstruction.forbrightness.astype(np.int16).copy() + brightness)
                Reconstruction.forcontrast  = img
                self.Reconstruction_holder.draw_image(img, 0, 255)

        except:
            pass

    def change_contrast(self, value):
        try:
            self.contrast_val_label.setText(str(self.contrast_Slider.value()) + " %")
            if Reconstruction.completed:
                brightness = int(250 * value / 100)
                img = (Reconstruction.forcontrast.astype(np.int16).copy() + brightness)
                Reconstruction.forbrightness = img
                self.Reconstruction_holder.draw_image(img, 0, 255)
        except:
            pass

    @staticmethod
    def is_prepared():
        return Reconstruction.image_opened and Reconstruction.sequence_prepared

    @staticmethod
    def store_slice(test_image):
        Reconstruction.test_image = test_image
        Reconstruction.forcontrast = test_image
        Reconstruction.forbrightness = test_image
        Reconstruction.image_opened = True
        Reconstruction.completed = False

    @staticmethod
    def store_squence(sequence):
        Reconstruction.sequence = sequence
        Reconstruction.sequence_prepared = True
