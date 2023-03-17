import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.animation as animation

plt.style.use('dark_background')
mpl.use('Qt5Agg')


class Viewer(FigureCanvas):

    def __init__(self, parent=None, width=0.1, height=0.01, dpi=100):
        self.fig = Figure()

        super().__init__(self.fig, )
        self.axes = self.fig.add_axes([0, 0, 1, 1])
        for spine in ['right', 'top', 'left', 'bottom']:
            self.axes.spines[spine].set_color('gray')

        self.axes.axis('off')
        self.rec = None

    def draw_image(self, img, vmin=None, vmax=None):
        self.axes.imshow(img, cmap='gray', vmin=vmin, vmax=vmax, aspect='auto')
        self.draw()

    def update_image(self, img):
        self.axes.imshow(img)
        self.draw()

    def clear_canvans(self):
        self.axes.clear()
        self.draw()

    def show_rectangle(self, startx, starty, width, height):
        self.rec = Rectangle((startx, starty), width, height, edgecolor="r", linewidth=1)
        Rectangle.set_fill(self.rec, False)
        self.axes.add_patch(self.rec)
        self.rec.set_visible(True)
        self.draw()

    def remove_rectangle(self):
        try:
            self.rec.remove()
            self.draw()

        except:
            pass


class Sequence_Drawer(FigureCanvas):
    def __init__(self, parent=None, width=0.1, height=0.01, dpi=100):
        self.fig, self.axes = plt.subplots(5, 1, sharex=True)
        self.axes[0].set_ylabel("RF", size=15)
        self.axes[1].set_ylabel("Slice", size=15)
        self.axes[2].set_ylabel("GY", size=15)
        self.axes[3].set_ylabel("Signal", size=15)
        self.axes[4].set_ylabel("Gx", size=15)

        super().__init__(self.fig)

    def draw_gx(self, te=0, gx=0):
        width = 0.15
        start = te - width / 2
        self.axes[4].clear()
        self.axes[4].set_ylabel("Gx", size=15)
        r = Rectangle((start, 0), width, 0.95 * gx, edgecolor='orange', linewidth=2)
        Rectangle.set_fill(r, False)
        self.axes[4].add_patch(r)
        self.draw()

    def draw_read_signal(self, te=0):
        start = te - 0.075
        end = te + 0.075
        x = np.linspace(start, end, 100)
        y = 0.85 * np.sinc(100 * (x - te))
        self.axes[3].clear()
        self.axes[3].set_xlim(left=0, right=1)
        self.axes[3].set_ylim(bottom=0, top=1)
        self.axes[3].plot(x, y, color="blue", linewidth=2)
        self.axes[3].set_ylabel("Signal", size=15)
        self.draw()

    def draw_slice_selection(self, slice):
        width = 0.15
        start = 0.004
        self.axes[1].clear()
        r = Rectangle((start, 0), width, 0.95 * slice, edgecolor='green', linewidth=2)
        self.axes[1].set_ylabel("Slice", size=15)
        Rectangle.set_fill(r, False)
        self.axes[1].add_patch(r)
        self.draw()

    def draw_rf(self, rf):
        start = 0
        end = 0.15
        x = np.linspace(start, end, 100)
        y = 0.85 * rf * np.sinc(100 * (x - 0.075))
        self.axes[0].clear()
        self.axes[0].set_xlim(left=0, right=1)
        self.axes[0].set_ylim(bottom=0, top=1)
        self.axes[0].plot(x, y, color="red", linewidth=2)
        self.axes[0].set_ylabel("RF", size=15)
        self.draw()

    def draw_gy(self, img_rows, gy):
        width = 0.15
        start = gy - width / 2
        delta_hight = 0.95 / img_rows
        self.axes[2].clear()
        self.axes[2].set_xlim(left=0, right=1)
        self.axes[2].set_ylim(bottom=0, top=1)
        for i in range(img_rows):
            hight = (i + 1) * delta_hight
            r = Rectangle((start, 0), width, hight, edgecolor='yellow')
            Rectangle.set_fill(r, False)
            self.axes[2].add_patch(r)
        self.axes[2].set_ylabel("Gy", size=15)
        self.draw()

    def animate_image(self, fig, update, init, frames):
        ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
        self.draw()
