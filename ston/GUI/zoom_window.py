"""
This file is part of the STON project (P.I. E. Dammer)
It creates the main window


Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""

####Standard Library
import os
from functools import partial

####python third party
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPlainTextEdit,\
                              QSizePolicy, QPushButton

from PIL import Image
from PIL.TiffTags import TAGS

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy

####Local imports
from . import slider
from ..utils import open_save_files
from ..processing import enhancers

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

        ###File
        self.file = None

        ###enhancers change states
        self.color = False
        self.brightness = False
        self.sharpness = False
        self.contrast = False

        ##Make the layout
        self.make_layout()

    def make_layout(self):
        '''
        Add widget to the window
        '''
        grid = QGridLayout()
        self.setLayout(grid)

        row = 0
        ###Qlabel for header
        header_label = QLabel('Header:')
        grid.addWidget(header_label, row, 0, 1, 1)
        row += 1

        ##PlainTextEdit for header
        self.header = QPlainTextEdit('Image header:')
        self.header.setReadOnly(True)
        self.header.setFixedWidth(250)
        self.header.setLineWrapMode(QPlainTextEdit.NoWrap)
        grid.addWidget(self.header, row, 0, 1, 1)
        row += 1

        ##Plot
        self.plot, self.fig, self.axs = self.create_plot()
        grid.addWidget(self.plot, 0, 1, 3, 8)

        ##live zoom Plot
        self.plot_zoom, self.zoom_fig, self.zoom_axs = self.create_plot()
        self.zoom_axs.axis('off')
        self.plot_zoom.setFixedWidth(250)
        self.plot_zoom.setFixedHeight(250)
        grid.addWidget(self.plot_zoom, row, 0, 1, 1)
        row += 1
        self.setMouseTracking(True)

        ##Notepad
        grid.addWidget(QLabel('Notes for this image:'), 0, 9, 1, 1)
        self.notepad = QPlainTextEdit()
        grid.addWidget(self.notepad, 1, 9, 2, 1)
        self.button_save_notes = QPushButton('Save Notes')
        grid.addWidget(self.button_save_notes, 3, 9, 1, 1)

        ##Enhancers labels
        grid.addWidget(QLabel('Color:'), 3, 1, 1, 1)
        grid.addWidget(QLabel('Contrast:'), 3, 3, 1, 1)
        grid.addWidget(QLabel('Brightness:'), 3, 5, 1, 1)
        grid.addWidget(QLabel('Sharpness:'), 3, 7, 1, 1)

        ##Enhancers sliders
        self.slider_color = slider.Slider()
        grid.addWidget(self.slider_color, 3, 2, 1, 1)

        self.slider_contrast = slider.Slider()
        grid.addWidget(self.slider_contrast, 3, 4, 1, 1)

        self.slider_brightness = slider.Slider()
        grid.addWidget(self.slider_brightness, 3, 6, 1, 1)

        self.slider_sharpness = slider.Slider()
        grid.addWidget(self.slider_sharpness, 3, 8, 1, 1)

        self.button_reset_enhancers = QPushButton('Reset Properties')
        grid.addWidget(self.button_reset_enhancers, row, 0, 1, 1)

        ###connect event
        self.slider_color.sliderReleased.connect(partial(self.slider_change, 'col'))
        self.slider_contrast.sliderReleased.connect(partial(self.slider_change, 'con'))
        self.slider_brightness.sliderReleased.connect(partial(self.slider_change, 'br'))
        self.slider_sharpness.sliderReleased.connect(partial(self.slider_change, 'sh'))
        self.button_reset_enhancers.clicked.connect(self.reset_sliders)
        self.button_save_notes.clicked.connect(self.save_notes)
        self.fig.canvas.mpl_connect('motion_notify_event', self.move_in_image)

        ##At startup, add the logo
        self.change_image(self.logo)

    def create_plot(self):
        '''
        This initialize the image plot
        '''
        #Create a matplotliub figure and axes isntance, witth the plotting parameters
        fig, axs = plt.subplots(1, 1, dpi=100)

        #Create the Matplotlib canvas widget, and add to parent layout
        canvas = FigureCanvas(fig)

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
        #update the file attribute
        self.file = file

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

        ##Update Notes
        ##clear the notepad
        self.notepad.clear()

        #Make the note file name ('image_name.notes')
        image_name = os.path.basename(file)
        note_file_name = image_name.split('.')[0] + '_ston_notes.txt'
        #Find the directory where the image is
        directory = os.path.dirname(file)
        ##Assemble final note name
        self.final_notes = os.path.join(directory, note_file_name)

        ###Check if it is there:
        if os.path.isfile(self.final_notes):
            ##Extract the text
            txt = open_save_files.open_txt_file(self.final_notes)
            ##add the notes
            self.notepad.setPlainText(txt)

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

    def slider_change(self, slider_name):
        '''
        This method process the enhancer valuesand process
        the images

        Parameters
        ----------
        slider_name :   str
                        name of the slider
        value       :   int
                        value of the slider that has moved 
        '''
        ##slider for color
        if slider_name == 'col':
            self.color = True

        elif slider_name == 'con':
            self.contrast = True

        ##slider for brightness
        elif slider_name == 'br':
            self.brightness = True

        ##slider for sharpness
        elif slider_name == 'sh':
            self.sharpness = True

        ########################
        ###Apply then changes###
        ########################

        ##image opening
        im = Image.open(self.file)

        ##Applied color change
        if self.color is True:
            color_im = enhancers.color(im, self.slider_color.value())
        else:
            color_im = im

        ##Apply contrast
        if self.contrast is True:
            contrast_im = enhancers.contrast(color_im, self.slider_contrast.value())
        else:
            contrast_im = color_im

        ##Apply brightness
        if self.brightness is True:
            brightness_im = enhancers.brightness(contrast_im, self.slider_brightness.value())
        else:
            brightness_im = contrast_im

        ##Apply sharpness
        if self.sharpness is True:
            sharpness_im = enhancers.sharpness(brightness_im, self.slider_sharpness.value())
        else:
            sharpness_im = brightness_im

        ###update the image
        self.axs.imshow(sharpness_im)

        ##redraw
        self.fig.tight_layout()
        self.plot.draw()

    def reset_sliders(self):
        '''
        This method reset all the slider to zero and reload the original
        image
        '''

        ##Reset the change states
        self.color = False
        self.brightness = False
        self.sharpness = False
        self.contrast = False

        ##put everything to zero
        self.slider_color.setValue(100)
        self.slider_contrast.setValue(100)
        self.slider_brightness.setValue(100)
        self.slider_sharpness.setValue(100)

        ##reload the original image
        self.change_image(self.file)

    def save_notes(self):
        '''
        This method saves the notes in a file
        Parameters
        ----------
        None

        Return
        ------
        None
        '''
        ##If we have some text to save
        if self.notepad.toPlainText():
            open_save_files.save_txt_to_file(self.final_notes, self.notepad.toPlainText())
