"""
This file is part of the STON project (P.I. E. Dammer)
It creates the image analysis window

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""

####Standard Library

####python third party
import numpy
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPlainTextEdit,\
                              QPushButton, QComboBox, QSpinBox, QTabWidget

####Local imports
from . import plots
from ..processing import enhancers
from ..processing import segmentation_regions

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
        self.move(400,400)
        self.conf = config
        self.resize(self.conf['Conf']['zoom_window_width'] + 200,
                    self.conf['Conf']['zoom_window_height'] + 400)
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

        reset_button = QPushButton('Reset to original')
        grid.addWidget(reset_button, row, 1, 1, 1)

        reset_to_cropped_button = QPushButton('Reset to Cropped')
        grid.addWidget(reset_to_cropped_button, row, 2, 1, 1)

        ###Gaussian filter
        gaussian_filter = QPushButton('Gaussian Filtering')
        grid.addWidget(gaussian_filter, row, 3, 1, 1)
        self.filtersigma = QSpinBox()
        grid.addWidget(self.filtersigma, row, 4, 1, 1)

        ##Run Chan Vese
        self.run_chan_vese = QPushButton('Run Chan Vese Segmentation')
        grid.addWidget(self.run_chan_vese, row, 9, 1, 2)
        
        row += 1

        ##Run region labelling
        self.run_region_label = QPushButton('Run Region identification')
        grid.addWidget(self.run_region_label, row, 9, 1, 2)
 

        ##create the place for each instrument tab
        self.tabbox = QTabWidget()
        self.tabbox.setTabsClosable(False)
        grid.addWidget(self.tabbox, row, 0, 7, 8)

        ###primary plot panel
        self.primary = Plot()
        self.tabbox.addTab(self.primary, 'Image to analyse')

        ##display the original image
        self.reset_image()

        ###Chan vese segmented
        self.chan_vese = Plot()
        self.tabbox.addTab(self.chan_vese, 'Chan Vese segmentation')

        ###Colored segmented plot panel
        self.region_plot = Plot()
        self.tabbox.addTab(self.region_plot, 'Region Plot')

        ###Colored segmented plot panel
        self.region_hist = Plot()
        self.tabbox.addTab(self.region_hist, 'Region histogram')

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
        reset_to_cropped_button.clicked.connect(self.reset_to_cropped)
        gaussian_filter.clicked.connect(self.apply_gaussian_filter)
        clr_txt_button.clicked.connect(self.clear_result_box)
        self.run_chan_vese.clicked.connect(self.run_chan_vese_seg)
        self.run_region_label.clicked.connect(self.run_region_id)

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
        self.primary.display_data(self.data_from_zoom_window)

    def reset_to_cropped(self):
        '''
        When the reset to crop button is used, we just reload the cropped image
        if it exists

        Parameter
        ---------
        none

        Return
        ------
        None 
        '''
        ##Check if a cropped image is used
        if hasattr(self, 'cropped_image'):
            ###display the data from zoom window
            self.primary.display_data(self.cropped_image)

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
        x0, xf = self.primary.axs.axes.get_xlim()
        yf, y0 = self.primary.axs.axes.get_ylim()

        ###crop the original image
        self.cropped_image = self.primary.ondisplay.get_array()[int(y0):int(yf), int(x0):int(xf)]

        ###display it
        self.primary.display_data(self.cropped_image)

        ###Write info the result box
        txt = f'Cropping image:\nx0={int(x0)}, xf={int(xf)}; y0={int(y0)}, yf={int(yf)} \n'
        txt2 = f'New size: x = {int(xf)-int(x0)}; y = {int(yf)-int(y0)}'
        self.write_to_result_box(txt + txt2)


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
        ondisplay = self.primary.ondisplay.get_array()

        ##apply filter
        filtered = enhancers.gaussian_filter(ondisplay, sigma)

        ##display it
        self.primary.display_data(filtered)

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

    def save_image(self, tab):
        '''
        This method saves the currently displayed image

        Parameter
        ---------
        None

        Return
        ------
        None
        '''

        ##get image
        ondisplay = self.primary.ondisplay.get_array()

    def run_chan_vese_seg(self):
        '''
        This method runs the Chan Vese segmentation
        it takes the image in the first panel and send it to
        the image analysis code

        Parameter
        ---------
        None

        Return
        ------
        None    
        '''
        ##get image
        ondisplay = self.primary.ondisplay.get_array()

        ##Chan Vese segementaiton
        chan_vese, results = segmentation_regions.apply_chan_vese(ondisplay)
        self.chan_vese.display_data(chan_vese, cmap='gray')

        ##Text to result box
        txt = 'Chan Vese Segmentation done (look at corresponfing panel):\n'
        txt += f"Ratio of black regions: {results['black']}\n"
        txt += f"Ratio of white regions: {results['white']}\n"
        self.write_to_result_box(txt)
 
    def run_region_id(self):
        '''
        This method runs the algorithm
        it takes the image in the first panel and send it to
        the image analysis code

        Parameter
        ---------
        None

        Return
        ------
        None    
        '''
        ##get image
        ondisplay = self.primary.ondisplay.get_array()

        ##Region segementaiton
        labeled_image, results,\
                       ratios = segmentation_regions.find_regions(ondisplay)
        self.region_plot.display_data(labeled_image, cmap='gray')
        self.region_plot.add_scatter(results, color='r')

        ##Text to result box
        txt = 'Region identification (look at corresponfing panel):\n'
        txt += f"Ratio of black regions: {ratios['black']}\n"
        txt += f"Ratio of white regions: {ratios['white']}\n"
        self.write_to_result_box(txt)
 


class Plot(QTabWidget):
    '''
    This class codes a simple panel with a plot inside
    '''
    def __init__(self):
        '''
        Class initialization
        Paramaeters
        -----------
        None
        '''
        ###create the tab
        QTabWidget.__init__(self)

        ##Make the grid
        grid = QGridLayout()
        self.setLayout(grid)

        ###Add the plot
        self.plot, self.fig, self.axs, self.toolbar = plots.create_plot(toolbar=True)
        self.axs.axis('off')
        grid.addWidget(self.plot, 0, 0, 7, 8)
        grid.addWidget(self.toolbar, 7, 0, 1, 6)

    def display_data(self, data, cmap=None):
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
        self.ondisplay = self.axs.imshow(data, cmap=cmap)

        ###Remove axis
        self.axs.axes.set_axis_off()

        ##Draw and adjust layout
        self.plot.draw()
        self.fig.tight_layout()

    def add_scatter(self, scatter, color=None):
        '''
        Add a data to self.axs as a scatter plot
        
        Parameters
        ----------
        scatter :   dict
                    with 'x' and 'y'

        Return
        ------
        None
        '''
        ##Add scatter plot
        self.axs.scatter(scatter['y'], scatter['x'], color=color,
                         marker='o', facecolors='none')

        ##Draw and adjust layout
        self.plot.draw()
        self.fig.tight_layout()
