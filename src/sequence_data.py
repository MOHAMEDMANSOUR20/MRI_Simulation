import json as js


class Sequence_Data:
    # RF degree ==> amp
    # Slice Selection ==> slope
    # TR
    # TE
    def __init__(self, RF=-1, Slice=-1, TR=-1, TE=-1):
        self.data = {"Sequence": {"RF": RF, "Slice": Slice, "TR": TR, "TE": TE}}

    def read_json(self, file):
        if self.data["Sequence"]["RF"] == -1:
            raise Exception("You can not read empty file!!!")

        with open(file, "r") as f:
            self.data = js.load(f)

    def export_json(self, file):
        with open(file, "w") as f:
            js.dump(self.data, f)
