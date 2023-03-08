import numpy as np
import math as m


class Rotation:

    def RX(self, theta):
        return np.array([[1, 0, 0],
                         [0, m.cos(theta), -m.sin(theta)],
                         [0, m.sin(theta), m.cos(theta)]])

    def RY(self, theta):
        return np.array([[m.cos(theta), 0, m.sin(theta)],
                         [0, 1, 0],
                         [-m.sin(theta), 0, m.cos(theta)]])

    def RZ(self, theta):
        return np.array([[m.cos(theta), -m.sin(theta), 0],
                         [m.sin(theta), m.cos(theta), 0],
                         [0, 0, 1]])
