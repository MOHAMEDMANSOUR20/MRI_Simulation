import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

plt.style.use('dark_background')
mpl.use('Qt5Agg')


class Viewer(FigureCanvas):

    def __init__(self, parent=None, width=0.1, height=0.01, dpi=100):
        self.fig = Figure()

        super().__init__(self.fig,)
        self.axes = self.fig.add_axes([0, 0, 1, 1])
        for spine in ['right', 'top', 'left', 'bottom']:
            self.axes.spines[spine].set_color('gray')

        self.axes.axis('off')


    def draw_image(self, img, vmin=None, vmax=None):
        self.axes.imshow(img, cmap='gray', vmin=vmin, vmax=vmax, aspect='auto')
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

class Sequence_Drawer(FigureCanvas):
    def __init__(self, parent=None, width=0.1, height=0.01, dpi=100):
        self.fig, self.axes = plt.subplots(5, 1, sharex=True)

        super().__init__(self.fig)


    def draw_gx(self, te=0, gx=0):
        width = 0.15
        start = te - width/2
        self.axes[4].clear()
        r = Rectangle((start, 0), width, gx, edgecolor='orange')
        Rectangle.set_fill(r, False)
        self.axes[4].add_patch(r)
        self.draw()



