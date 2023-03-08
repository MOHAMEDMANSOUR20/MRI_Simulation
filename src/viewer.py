import matplotlib as matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use('dark_background')
matplotlib.use('Qt5Agg')



class Viewer(FigureCanvas):

    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = Figure()
        super().__init__(self.fig) 
        self.axes = self.fig.add_axes([0,0,1,1])
        for spine in ['right', 'top', 'left', 'bottom']:
            self.axes.spines[spine].set_color('gray')
       
        self.axes.axis('off')

    def draw_image(self,img,vmin=0, vmax=255):
        self.axes.imshow(img, cmap='gray', aspect='auto', vmin=vmin, vmax=vmax)
        self.draw()

   

    
 


        

    


    def update_image(self, img):
        self.axes.imshow(img)
        self.draw()


    def clear_canvans(self):
        self.axes.clear()
        self.draw()

    def draw_histogram(self, img):

        self.axes.hist(img, bins=5)
        self.draw()