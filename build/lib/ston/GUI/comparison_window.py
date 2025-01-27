"""
This file is part of the STON project (P.I. E. Dammer)
It creates the side by side comparison window


Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
"""

####Standard Library
from functools import partial
import os

####python third party
import numpy
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox

from PIL import Image

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

        ###adjust the window
        self.resize(config['Conf']['compare_window_width'], config['Conf']['compare_window_height'])
        self.move(400,400)

        ###create some attributes
        self.images = images_with_path
        self.setWindowTitle('STON: Comparison: ' +
                           f'{images_without_path[0]} and {images_without_path[1]}')
        self.data1 = None
        self.data2 = None

        ###add all the widgets
        self.make_layout()

        ###set up zoom and primary plot
        self.setup_common_zoom_and_primary_plot()

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
        self.choice.addItems(['Yes', 'No'])
        grid.addWidget(self.choice, row, 1, 1, 1)

        ###Label for primary plot
        primary_plot = QLabel('Primary plot?')
        grid.addWidget(primary_plot, row, 2, 1, 1)

        ###Choice of primary plot
        self.primary = QComboBox()
        self.primary.addItems(['Top', 'Bottom'])
        grid.addWidget(self.primary, row, 3, 1, 1)

        ###Connect events
        self.plot1.mpl_connect('motion_notify_event', partial(self.crosshair)) ###Crosshair on plot
        self.plot2.mpl_connect('motion_notify_event', partial(self.crosshair)) ###Crosshair on plot
        self.choice.currentTextChanged.connect(self.setup_common_zoom_and_primary_plot)
        self.primary.currentTextChanged.connect(self.setup_common_zoom_and_primary_plot)

    def setup_common_zoom_and_primary_plot(self):
        '''
        Select the plot that controls the zoom on both plots 

        Parameters
        ----------
        None

        Return
        ------
        None
        '''
        ###check if we do a common zoom
        if self.choice.currentText() == 'Yes':

            ###if yes we check what plot is primary
            if self.primary.currentText() == 'Top':
                ###if it is the top one we must track the changes on the top one
                ###And disconnect the bottom one
                if hasattr(self, 'callback_y_bottom'):
                    self.axs2.callbacks.disconnect(self.callback_x_bottom)
                    self.axs2.callbacks.disconnect(self.callback_y_bottom)
                    delattr(self, 'callback_y_bottom')
                    delattr(self, 'callback_x_bottom')

                ###and then create the connect the axis to the function
                self.callback_x_top = \
                        self.axs1.callbacks.connect('xlim_changed',
                                                    partial(self.change_limits, 'Top'))

                self.callback_y_top = \
                        self.axs1.callbacks.connect('ylim_changed',
                                                    partial(self.change_limits, 'Top'))

            else:
                ###Same if it is the bottom one
                if hasattr(self, 'callback_y_top'):
                    self.axs1.callbacks.disconnect(self.callback_x_top)
                    self.axs1.callbacks.disconnect(self.callback_y_top)
                    delattr(self, 'callback_y_top')
                    delattr(self, 'callback_x_top')

                self.callback_x_bottom = \
                        self.axs2.callbacks.connect('xlim_changed',
                                                    partial(self.change_limits, 'Bottom'))

                self.callback_y_bottom = \
                        self.axs2.callbacks.connect('ylim_changed',
                                                    partial(self.change_limits, 'Bottom'))

        else: ###<---If the common zoom is set to 'No'

            ###Disconnect the events
            if hasattr(self, 'callback_y_bottom'):
                self.axs2.callbacks.disconnect(self.callback_x_bottom)
                self.axs2.callbacks.disconnect(self.callback_y_bottom)

            if hasattr(self, 'callback_y_top'):
                self.axs1.callbacks.disconnect(self.callback_x_top)
                self.axs1.callbacks.disconnect(self.callback_y_top)


    def change_limits(self, plot_id, axs):
        '''
        When the limits on a plot are changed, we changed the limis of the
        other plots accordingly. This happens only if the common zoom option
        is used.

        Parameters
        ----------
        plotID      str
                    name of the plot it comes from
        axs         matplotlib axes
                    plot where the changes has been made

        Return
        ------
        None
        '''
        ##get the x and y limits
        new_x_min, new_x_max = axs.get_xlim()
        new_y_min, new_y_max = axs.get_ylim()

        if plot_id == 'Top':
            ###check we are ok wrt plot2 limits
            self.axs2.set_xlim((new_x_min, new_x_max))
            self.axs2.set_ylim((new_y_min, new_y_max))
            self.fig2.tight_layout()
            self.plot2.draw()

        ###Check what plots we changed
        if plot_id == 'Bottom':
            ###check we are ok wrt plot1 limits
            self.axs1.set_xlim((new_x_min, new_x_max))
            self.axs1.set_ylim((new_y_min, new_y_max))
            self.fig1.tight_layout()
            self.plot1.draw()

    def crosshair(self, event):
        '''
        This method draws the crosshair on both plot

        Parameters
        ----------
        event   :   matplotlib MouseEvent
                    holds the position of the mouse on the plot            

        Return
        ------
        None
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
            self.axs1.imshow(self.data1)

            ##display the name of the image:
            name = os.path.basename(file)
            self.axs1.text(0, 0, f'{name}', transform=self.axs1.transAxes, color='w')

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
            name = os.path.basename(file)
            self.axs2.text(0, 0, f'{name}', transform=self.axs2.transAxes, color='w')

            ##redraw
            self.fig2.tight_layout()
            self.plot2.draw()
