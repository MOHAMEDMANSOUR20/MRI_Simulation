import json as js
from PyQt5 import QtWidgets as qtw


class Sequence_Data:
    # RF degree ==> amp
    # Slice Selection ==> slope
    # TR
    # TE
    def __init__(self, RF=0, Slice=0, TR=0, TE=0, GY=0, GX=0):
        self.data = {"Sequence": {"RF": RF, "Slice": Slice, "TR": TR, "TE": TE, "GY":GY, "GX":GX}}

    def read_json(self, file):
        #if self.data["Sequence"]["RF"] == -1:
            #raise Exception("You can not read empty file!!!")

        with open(file, "r") as f:
            self.data = js.load(f)

    def export_json(self, file):

        with open(file, "w") as f:
            js.dump(self.data, f)
