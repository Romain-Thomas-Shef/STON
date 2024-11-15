"""
This file is part of the STON project (P.I. E. Dammer)
It creates the side by side comparison window


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
from PySide6.QtWidgets import QWidget, QGridLayout, QSizePolicy

from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy



class CompareWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, config, images_with_path, images_without_path):
        '''
        Class constructor
        
        Parameter
        ---------
        config  :dict
                 configuration dictionary

        images_with_path: list
                          list of files with their path

        images_without_path:    list
                                list of image names

        Return
        ------
        None
        '''
        super().__init__()

        ###
        self.resize(config['Conf']['compare_window_width'], config['Conf']['compare_window_height'])
        self.move(400,400)
        self.images = images_with_path
        self.setWindowTitle('STON: Comparison: ' +
                           f'{images_without_path[0]} and {images_without_path[1]}')
        self.data1 = None
        self.data2 = None
        self.parent()
        self.make_layout()

    def make_layout(self):
        '''
        This method organises the widgets
        Parameter
        ---------
        None

        Return
        ------
        None
        '''

        left_grid = QGridLayout()
        self.setLayout(left_grid)


        self.plot1, self.fig1, self.axs1 = self.create_plot()
        self.change_image(self.images[0], 1)
        left_grid.addWidget(self.plot1, 0, 1, 2, 1)

        self.plot2, self.fig2, self.axs2 = self.create_plot()
        self.change_image(self.images[1], 2)
        left_grid.addWidget(self.plot2, 2, 1, 2, 1)

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

    def change_image(self, file, n):
        '''
        This is triggered when a single image is double clicked on 

        Parameter
        ---------
        path:  str
                    path to image
            
        n   :   int
                plot number to change
        Return
        ------
        None
        '''
        ##open image
        image = Image.open(file)

        if n == 1:
            ##clear the plot
            self.axs1.cla()

            ##remove axis
            self.axs1.axis('off')

            ##display it
            self.data1 = numpy.array(image)
            self.axs1.imshow(self.data1)

            ##display the name of the image:
            self.axs1.text(0, 0, f'{file}', transform=self.axs1.transAxes)

            ##redraw
            self.fig1.tight_layout()
            self.plot1.draw()

        if n == 2:
            ##clear the plot
            self.axs2.cla()

            ##remove axis
            self.axs2.axis('off')

            ##display it
            self.data2 = numpy.array(image)
            self.axs2.imshow(self.data2)

            ##display the name of the image:
            self.axs2.text(0, 0, f'{file}', transform=self.axs2.transAxes)

            ##redraw
            self.fig2.tight_layout()
            self.plot2.draw()
