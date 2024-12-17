"""
This file is part of the STON project (P.I. E. Dammer)
It creates the main window


Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
version: 0.1

changelog:
----------
0.1: RTh - Create the file
"""

####Standard Library
import os

####python third party
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPlainTextEdit, QSizePolicy

from PIL import Image
from PIL.TiffTags import TAGS

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy

####Local imports


class DetailWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, logo, config):
        '''
        Class constructor
        '''
        super().__init__()
        self.hidden = True
        self.move(200,200)
        self.conf = config['Conf']
        self.resize(self.conf['zoom_window_width'], self.conf['zoom_window_height'])
        self.setWindowTitle('STON: Detail window')
        self.logo = logo
        self.make_layout()

    def make_layout(self):
        '''
        Add widget to the window
        '''
        left_grid = QGridLayout()
        self.setLayout(left_grid)

        row = 0
        ###Qlabel for header
        header_label = QLabel('Header:')
        left_grid.addWidget(header_label, row, 0, 1, 1)
        row += 1

        ##PlainTextEdit for header
        self.header = QPlainTextEdit('Image header:')
        self.header.setReadOnly(True)
        self.header.setFixedWidth(250)
        #header.setFixedHeight(300)
        self.header.setLineWrapMode(QPlainTextEdit.NoWrap)
        left_grid.addWidget(self.header, row, 0, 1, 1)
        row += 1

        ##Plot
        self.plot, self.fig, self.axs = self.create_plot()
        self.change_image(self.logo)
        left_grid.addWidget(self.plot, 0, 1, 3, 2)
        self.connect_cursor_click()


        ##live zoom Plot
        self.plot_zoom, self.zoom_fig, self.zoom_axs = self.create_plot()
        self.zoom_axs.axis('off')
        #self.change_image(self.logo)
        self.plot_zoom.setFixedWidth(250)
        self.plot_zoom.setFixedHeight(250)
        left_grid.addWidget(self.plot_zoom, row, 0, 1, 1)

        ##QLabel for zoom
        #self.zoom = QLabel()
        #pixmap = QtGui.QPixmap(self.logo)
        #scaled = pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        #self.zoom.setPixmap(scaled)
        #left_grid.addWidget(self.zoom, row, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        #Track the motion of the cursor in the original 2D image
        self.setMouseTracking(True)


        ###connect event
        self.fig.canvas.mpl_connect('motion_notify_event', self.move_in_image)

    def create_plot(self):
        '''
        This initialize the image plot
        '''
        #Create a matplotliub figure and axes isntance, witth the plotting parameters
        fig, axs = plt.subplots(1, 1, dpi=100)

        #Create the Matplotlib canvas widget, and add to parent layout
        canvas = FigureCanvas(fig)

        #SOme widget resizing code, not sure what it does but was in a tutorial... TO be removed?
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()
        return canvas, fig, axs

    def change_image(self, file):
        '''
        This is triggered when a single image is double clicked on 

        Parameter
        ---------
        path:  str
                    path to image

        Return
        ------
        None
        '''
        ##open image
        image = Image.open(file)

        ##clear the header
        self.header.clear()
        ##get the extnsion of the file
        _, extension = os.path.splitext(file)
        ###get the header
        if extension == '.tif':
            header = {TAGS[key] : image.tag[key] for key in image.tag_v2}
            for i in header:
                text = f"{i[:17]:<20} \t{str(header[i]).replace('(','').replace(')','')}"
                self.header.appendPlainText(text)
        else:
            text = f'No header display for {extension} extensions.'
            self.header.appendPlainText(text)

        ##clear the plot
        self.axs.cla()

        ##remove axis
        self.axs.axis('off')

        ##display it
        self.data = numpy.array(image)
        self.axs.imshow(self.data)

        ##redraw
        self.fig.tight_layout()
        self.plot.draw()

    def connect_cursor_click(self):
        '''
        Start the event handler for cursor left click.
        Returns
        -------

        '''

        # Start the event handler for cursor motion in the original 2D image


    def move_in_image(self, event):
        '''
        Function to execute when the cursor position is updated: store the cursor position
        and redraw the zoomed-in image in the source_picker widget
        Parameters
        ----------
        event (matplotlib motion_notify_event) - matplotlib event instance from cursor movement

        Returns
        -------

        '''
        #Make sure the cursor is in the matplolib axes of the original 2D image
        if event.inaxes == self.axs:
            #Store the coordinates of the cursor
            self.xcursorloc = event.xdata
            self.ycursorloc = event.ydata
            #Update the zoom-in display of source_picker
            self.update_picker_display()



    def update_picker_display(self):
        '''
        Update the zoom-in 2D display of the image in the source_picker window

        Returns
        -------

        '''

        self.zoom_axs.cla()
        #Obtain the original 2D image data and plot in source_picker widget
        self.maxx = self.data.shape[0]
        self.maxy = self.data.shape[1]
        self.zoom_axs.imshow(self.data, rasterized=True, origin='lower')

        self.winsize = self.conf['zoom_insert_pix_size']
        #Zoom-in on original 2D image data according to size obtained from the sliding bar
        xmin, xmax = self.xcursorloc - 0.5 * self.winsize, self.xcursorloc + 0.5 * self.winsize
        ymin, ymax = self.ycursorloc - 0.5 * self.winsize, self.ycursorloc + 0.5 * self.winsize

        #Make sure the zoomed-in display window shows a
        #full image in the corner, and not blank space
        if xmin < 0:
            xmin = 0
            xmax = self.winsize
        elif xmax > self.data.shape[1]:
            xmax = self.data.shape[1]
            xmin = xmax - self.winsize
        if ymin < 0:
            ymin = 0
            ymax = self.winsize
        elif ymax > self.data.shape[0]:
            ymax = self.data.shape[0]
            ymin = ymax - self.winsize

        self.zoom_axs.set_xlim(xmin, xmax)
        self.zoom_axs.set_ylim(ymax, ymin)
        self.zoom_axs.axis('off')
        self.zoom_fig.canvas.draw()
