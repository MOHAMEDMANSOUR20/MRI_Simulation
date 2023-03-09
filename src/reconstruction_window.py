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
    sequence = { }

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
            phantom_img = Reconstruction.test_image
            num_row = phantom_img.shape[0]
            num_column = phantom_img.shape[1]
            img_vectors = np.ones((num_row, num_column, 3))
            img_vectors[:, :, 2] = img_vectors[:, :, 2] * phantom_img
            img_vectors[:, :, 0] = 0
            img_vectors[:, :, 1] = 0
            R_forRF = self.Rotation_matrix.RX(self.PI / 2).T
            img_vectors = np.matmul(img_vectors[:], R_forRF)
            step_inGY = 2 * self.PI / num_row
            step_inGx = 2 * self.PI / num_column
            img_vector_changed = img_vectors
            vector_summation = []
            for i in range(num_row):
                step_y_inner = (step_inGY * (i + 1)) / num_row
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
            self.Reconstruction_holder.clear_canvans()
            self.K_Space_holder.clear_canvans()
            self.K_Space_holder.draw_image(vector_summation)
            reconstructed_slice = np.abs(np.fft.ifft(vector_summation))
            self.Reconstruction_holder.draw_image(reconstructed_slice)
        else:
            QtWidgets.QMessageBox.about(
                self, "Error", "Open phantom first")

    @staticmethod
    def is_prepared():
        return Reconstruction.image_opened and Reconstruction.sequence_prepared

    @staticmethod
    def store_slice(test_image):
        Reconstruction.test_image = test_image
        Reconstruction.image_opened = True
    @staticmethod
    def store_squence(sequence):
        Reconstruction.sequence = sequence
        Reconstruction.sequence_prepared = True
