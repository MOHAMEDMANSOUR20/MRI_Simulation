import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from sequence_data import Sequence_Data
from viewer import Viewer


class Sequence_Controller(qtw.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi("ui/sequence_control_widget.ui", self)
        self.json_file = Sequence_Data()
        self.export_Button.clicked.connect(self.export_sequence)


    def export_sequence(self):
        default_dir = "jsons"
        file_name, _ = qtw.QFileDialog.getSaveFileName(self, "save json file", default_dir, "Text files (*.json)")
        file = os.path.join(default_dir, file_name)
        self.json_file.export_json(file)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main = Sequence_Controller()
    main.show()
    sys.exit(app.exec_())