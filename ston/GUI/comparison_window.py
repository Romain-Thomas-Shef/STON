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
from functools import partial

####python third party
import numpy
from PySide6.QtWidgets import QWidget, QGridLayout, QSizePolicy, QPushButton, QLabel,\
                              QComboBox

from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

##Local imports
from . import plots


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
        self.updated_axes = False
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

        grid = QGridLayout()
        self.setLayout(grid)
        row = 0

        self.plot1, self.fig1, self.axs1, self.toolbar1 = plots.create_plot(toolbar=True)
        self.change_image(self.images[0], 1)
        grid.addWidget(self.plot1, row, 0, 2, 8)
        row += 2
        grid.addWidget(self.toolbar1, row, 6, 1, 2)
        row += 1
        
        self.plot2, self.fig2, self.axs2, self.toolbar2 = plots.create_plot(toolbar=True)
        self.change_image(self.images[1], 2)
        grid.addWidget(self.plot2, row, 0, 2, 8)
        row += 2 
        grid.addWidget(self.toolbar2, row, 6, 1, 2)

        ###Label for common zoom
        common_zoom = QLabel('Common zoom?')
        grid.addWidget(common_zoom, row, 0, 1, 1)

        ###Choice yes or no
        self.choice = QComboBox()
        self.choice.addItems(['No', 'Yes'])
        grid.addWidget(self.choice, row, 1, 1, 1)

        ###Label for common zoom
        primary_plot = QLabel('Primary plot?')
        grid.addWidget(primary_plot, row, 2, 1, 1)

        ###Choice yes or no
        self.primary = QComboBox()
        self.primary.addItems(['Top', 'Bottom'])
        grid.addWidget(self.primary, row, 3, 1, 1)


        
        ###Connect events
        self.plot1.mpl_connect('motion_notify_event', partial(self.crosshair))
        self.plot2.mpl_connect('motion_notify_event', partial(self.crosshair))
        self.axs1.callbacks.connect('xlim_changed', partial(self.change_limits, 'plot1'))
        self.axs1.callbacks.connect('ylim_changed', partial(self.change_limits, 'plot1'))
        #self.axs2.callbacks.connect('xlim_changed', partial(self.change_limits, 'plot2'))
        #self.axs2.callbacks.connect('ylim_changed', partial(self.change_limits, 'plot2'))

    def change_limits(self, plotID, axs):
        '''
        test
        '''
        ##get the x and y limits
        new_x_min, new_x_max = self.axs1.get_xlim()
        new_y_min, new_y_max = self.axs1.get_ylim()
        print(plotID, self.updated_axes) 
        ###Check what plots we changed
        if plotID == 'plot1':
            ###check we are ok wrt plot2 limits
            if  new_x_max  < self.data2.shape[1] and new_y_max < self.data2.shape[0] and self.updated_axes is False:
                self.axs2.set_xlim((new_x_min, new_x_max))
                self.axs2.set_ylim((new_y_min, new_y_max))
                self.fig2.tight_layout()
                self.plot2.draw()

        ###Check what plots we changed
        if plotID == 'plot2':
            ###check we are ok wrt plot1 limits
            if  new_x_max  < self.data1.shape[1] and new_y_max < self.data1.shape[0] and self.updated_axes is False:
                self.axs1.set_xlim((new_x_min, new_x_max))
                self.axs1.set_ylim((new_y_min, new_y_max))
                self.fig1.tight_layout()
                self.plot1.draw()
                self.updated_axes = True

    def crosshair(self, event):
        '''
        This method draw the crosshair on both plot
        '''
        ##check that some coordinate are available.
        if event.xdata is not None and event.ydata is not None:
            ##remove the previous lines
            if len(self.axs1.lines) > 0:
                self.axs1.lines[-1].remove()
                self.axs1.lines[-1].remove()
            if len(self.axs2.lines) > 0:
                self.axs2.lines[-1].remove()
                self.axs2.lines[-1].remove()
        
            ##get the position of the cursor
            x = float(event.xdata)
            y = float(event.ydata)

            ##Draw the crosshair
            crosshair_color = 'red'

            ####if coordinate inside the image we draw
            if 0 < x < self.data1.shape[1] and 0 < y < self.data1.shape[0]:                       
                self.axs1.axhline(y, lw=0.8, color=crosshair_color)
                self.axs1.axvline(x, lw=0.8, color=crosshair_color)
                self.fig1.tight_layout()
                self.plot1.draw()

            ####same for second plot
            if 0 < x < self.data2.shape[1] and 0 < y < self.data2.shape[0]:                       
                self.axs2.axhline(y, lw=0.8, color=crosshair_color)
                self.axs2.axvline(x, lw=0.8, color=crosshair_color)
                self.fig2.tight_layout()
                self.plot2.draw()


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
            self.axs1.imshow(self.data1, origin='lower')

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
            self.axs2.imshow(self.data2, origin='lower')

            ##display the name of the image:
            self.axs2.text(0, 0, f'{file}', transform=self.axs2.transAxes)

            ##redraw
            self.fig2.tight_layout()
            self.plot2.draw()
