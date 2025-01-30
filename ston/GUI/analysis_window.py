"""
This file is part of the STON project (P.I. E. Dammer)
It creates the image analysis window

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""

####Standard Library

####python third party
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPlainTextEdit,\
                              QPushButton, QComboBox, QSpinBox

####Local imports
from . import plots
from ..processing import enhancers

class AnalysisWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, config, data):
        '''
        Class constructor
        '''
        super().__init__()
        self.hidden = True
        self.move(200,200)
        self.conf = config
        self.resize(self.conf['Conf']['zoom_window_width'],
                    self.conf['Conf']['zoom_window_height'])
        self.setWindowTitle('STON: Analyse Image')

        ##the image data
        self.data_from_zoom_window = data

        ##Make the layout
        self.make_layout()

    def make_layout(self):
        '''
        Add widget to the window
        '''
        grid = QGridLayout()
        self.setLayout(grid)

        #initialize row
        row = 0

        ##Crop button
        crop_button = QPushButton('Crop image')
        grid.addWidget(crop_button, row, 0, 1, 1)

        reset_button = QPushButton('Reset image')
        grid.addWidget(reset_button, row, 1, 1, 1)

        ###Gaussian filter
        gaussian_filter = QPushButton('Gaussian Filtering')
        grid.addWidget(gaussian_filter, row, 2, 1, 1)
        self.filtersigma = QSpinBox()
        grid.addWidget(self.filtersigma, row, 3, 1, 1)

        ##Algorithm
        grid.addWidget(QLabel('Choose Segmentation Algorithm:'), row, 5, 1, 2)
        self.algo_choice = QComboBox()
        self.algo_choice.addItem('Random Walker')
        self.algo_choice.addItem('Chan Vese')
        grid.addWidget(self.algo_choice, row, 9, 1, 2)
        row += 1
        self.run = QPushButton('Run algorithm')
        grid.addWidget(self.run, row, 9, 1, 2)

        ##Plot
        self.plot, self.fig, self.axs, self.toolbar = plots.create_plot(toolbar=True)
        self.axs.axis('off')
        grid.addWidget(self.plot, row, 0, 7, 8)
        grid.addWidget(self.toolbar, row+7, 0, 1, 4)

        ##display
        self.reset_image()

        ##Result box
        self.results = QPlainTextEdit()
        self.results.setReadOnly(True)
        self.results.setFixedWidth(250)
        grid.addWidget(self.results, row+1, 9, 6, 2)

        ###save image button
        save_image_button = QPushButton('Save image')
        grid.addWidget(save_image_button, row+7, 6, 1, 2)

        ###save image button
        save_txt_button = QPushButton('Save text')
        grid.addWidget(save_txt_button, row+7, 10, 1, 1)

        ###clear txt image button
        clr_txt_button = QPushButton('Clear text')
        grid.addWidget(clr_txt_button, row+7, 9, 1, 1)

        ##Connect signals
        crop_button.clicked.connect(self.crop_image)
        reset_button.clicked.connect(self.reset_image)
        gaussian_filter.clicked.connect(self.apply_gaussian_filter)
        clr_txt_button.clicked.connect(self.clear_result_box)

    def reset_image(self):
        '''
        When the reset image is used, we just reload the image the was sent
        to this window (self.data_from_zoom_window).

        Parameter
        ---------
        none

        Return
        ------
        None 
        '''
        ###display the data from zoom window
        self.display_data(self.data_from_zoom_window)

    def crop_image(self):
        '''
        To crop an image, the user must use the matplotlib lense button
        button to adjust the size of the image.
        Once done, the crop image button send the the flow here
        we look at the nuwe limits of the plot and create a new iamge
        from these limits.
        and we display the new image


        Parameter
        ---------
        none

        Return
        ------
        None
        '''

        ##Extract new limits
        x0, xf = self.axs.axes.get_xlim()
        yf, y0 = self.axs.axes.get_ylim()

        ###crop the original image
        data = self.ondisplay.get_array()[int(y0):int(yf), int(x0):int(xf)]

        ###display it
        self.display_data(data)

        ###Write info the result box
        txt = f'Cropping image:\nx0={int(x0)}, xf={int(xf)}; y0={int(y0)}, yf={int(yf)} \n'
        txt2 = f'New size: x = {int(xf)-int(x0)}; y = {int(yf)-int(y0)}'
        self.write_to_result_box(txt + txt2)

    def display_data(self, data):
        '''
        Display data in the plot area

        Parameter
        ---------
        data    :   numpy array
                    data to display

        Return
        ------
        None 
        '''
        ##clear the plot
        self.fig.clf()
        self.axs = self.fig.add_subplot()

        ###Display
        self.ondisplay = self.axs.imshow(data)

        ###Remove axis
        self.axs.axes.set_axis_off()

        ##Draw and adjust layout
        self.plot.draw()
        self.fig.tight_layout()


    def apply_gaussian_filter(self):
        '''
        This method applies a gaussian filter
        Parameter
        ---------
        none

        Return
        ------
        None 
        '''
        ###Get sigma
        sigma = self.filtersigma.value()

        ##get image
        ondisplay = self.ondisplay.get_array()

        ##apply filter
        filtered = enhancers.gaussian_filter(ondisplay, sigma)

        ##display it
        self.display_data(filtered)

        ###Write info the result box
        txt = f'Gaussian filter:\nsigma={sigma}'
        self.write_to_result_box(txt)



    def write_to_result_box(self, text):
        '''
        This method writes in the result box on the right

        Parameter
        ---------
        text        :   str
                        text to write
        
        Return
        ------
        None
        '''
        ###We always break a line at the end.
        self.results.appendPlainText(text + '\n')

    def clear_result_box(self):
        '''
        This method clears the result box (removes all the txt)

        Parameter
        ---------
        None

        Return
        ------
        None
        '''
        self.results.clear()

    def save_image(self):
        '''
        This method saves the currently displayed image

        Parameter
        ---------
        None

        Return
        ------
        None
        '''
        self.results.clear()
