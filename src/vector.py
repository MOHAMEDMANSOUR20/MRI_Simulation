import numpy as np    

class Vector:

  def __init__(self, x, y, z,T1,T2,PD):
    self.vec = np.array([x,y,z])
    self.data = np.array([z,T1,T2,PD])


    def intensity_value(self):
        return self.data[0]

    def t1_value(self):
        return self.data[1]

    def t2_value(self):
        return self.data[2]

    def pd_value(self):
        return self.data[3]