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

####python third party
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPlainTextEdit, QSizePolicy

from PIL import Image
from PIL.TiffTags import TAGS

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

####Local imports


class DetailWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, logo):
        '''
        Class constructor
        '''
        super().__init__()
        self.hidden = True
        self.move(200,200)
        self.setWindowTitle('STON: Detail window')
        self.logo = logo
        self.make_layout()

        ###fixe the size of the window
        #self.setFixedSize(self.width(), self.height())


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
        self.plot = self.create_plot()
        self.change_image(self.logo)
        left_grid.addWidget(self.plot, 0, 1, 3, 2)

        ##QLabel for zoom
        self.zoom = QLabel()
        pixmap = QtGui.QPixmap(self.logo)
        scaled = pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom.setPixmap(scaled)
        left_grid.addWidget(self.zoom, row, 0, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    def create_plot(self):
        '''
        This initialize the image plot
        '''
        #Create a matplotliub figure and axes isntance, witth the plotting parameters
        self.fig, self.axs = plt.subplots(1, 1, dpi=100)

        #Create the Matplotlib canvas widget, and add to parent layout
        canvas = FigureCanvas(self.fig)

        #SOme widget resizing code, not sure what it does but was in a tutorial... TO be removed?
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()
        return canvas

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

        ##get header
        self.header.clear()
        if file.split('.')[-1] == 'tif':
            header = {TAGS[key] : image.tag[key] for key in image.tag_v2}
            for i in header:
                text = f"{i[:15]:<20} \t{str(header[i]).replace('(','').replace(')','')}"
                self.header.appendPlainText(text)

        ##clear the plot
        self.axs.cla()

        ##remove axis
        self.axs.axis('off')

        ##display it
        self.axs.imshow(image)

        ##redraw
        self.fig.tight_layout()
        self.plot.draw()
