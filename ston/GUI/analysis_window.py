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
                              QPushButton, QSpinBox, QTabWidget, QFileDialog
from matplotlib import patches

####Local imports
from . import plots
from ..utils import open_save_files
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
        self.resize(self.conf['Conf']['analysis_window_width'],
                    self.conf['Conf']['analysis_window_height'])
        self.setWindowTitle('STON: Analyse Image')

        ##the image data
        self.data_from_zoom_window = data

        ###An empty results dictionary
        self.results = {}

        ###get converstion factor
        pix_to_mm = self.conf['Analysis']['pix_to_mm']
        ##areas are in number of pixel, so to get an area in mm2 we need
        self.conversion_area = pix_to_mm * pix_to_mm

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


        ##Run region labelling
        self.run_region_label = QPushButton('Run Region identification')
        grid.addWidget(self.run_region_label, row, 9, 1, 2)

        row += 1

        ##create the place for each instrument tab
        self.tabbox = QTabWidget()
        self.tabbox.setTabsClosable(False)
        grid.addWidget(self.tabbox, row, 0, 7, 8)

        ###primary plot panel
        self.primary = Plot()
        self.tabbox.addTab(self.primary, 'Image to analyse')

        ##display the original image
        self.reset_image()

        ###Colored segmented plot panel
        self.region_plot = Plot(allregions=True, conversion=self.conversion_area)
        self.tabbox.addTab(self.region_plot, 'Region Plot')

        ###Colored segmented plot panel
        self.region_hist = Plot()
        self.tabbox.addTab(self.region_hist, 'Region histogram')
        self.region_hist.display_data(clear = True, datatype='empty')

        ###Colored segmented plot panel
        self.indiv_region_plot = Plot(explorer=True,
                                      results_box_write=self.write_to_result_box,
                                      conversion=self.conversion_area)
        self.tabbox.addTab(self.indiv_region_plot, 'Explore Regions')

        ##Result box
        self.resultsbox = QPlainTextEdit()
        self.resultsbox.setReadOnly(True)
        self.resultsbox.setFixedWidth(250)
        grid.addWidget(self.resultsbox, row, 9, 7, 2)

        ###save text button
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
        reset_to_cropped_button.clicked.connect(self.reset_to_cropped)
        gaussian_filter.clicked.connect(self.apply_gaussian_filter)
        clr_txt_button.clicked.connect(self.clear_result_box)
        save_txt_button.clicked.connect(self.save_result_box)
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
        self.primary.display_data(self.data_from_zoom_window, clear=True)

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
            self.primary.display_data(self.cropped_image, clear=True)
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
        x0, xf = self.primary.axs.axes.get_xlim()
        yf, y0 = self.primary.axs.axes.get_ylim()

        ###crop the original image
        self.cropped_image = self.primary.ondisplay.get_array()[int(y0):int(yf), int(x0):int(xf)]

        ###display it
        self.primary.display_data(self.cropped_image, clear=True)

        ###Write info the result box
        txt = f'Cropping image:\nx0={int(x0)}, xf={int(xf)}; y0={int(y0)}, yf={int(yf)} \n'
        txt += f'New size: x = {int(xf)-int(x0)}; y = {int(yf)-int(y0)}\n'
        txt += f'Area = {(int(xf)-int(x0))*(int(yf)-int(y0))}'
        self.write_to_result_box(txt)

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
        ondisplay = self.primary.ondisplay.get_array()

        ##apply filter
        filtered = enhancers.gaussian_filter(ondisplay, sigma)

        ##display it
        self.primary.display_data(filtered, clear=True)

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
        self.resultsbox.appendPlainText(text + '\n')

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
        self.resultsbox.clear()

    def save_result_box(self):
        '''
        This method writes the result box into a file
        It calls the a filedialog to choose the file
        and then use the generic file save function
        to save evertyhing.
        
        Parameters
        ----------
        None
        
        Return
        ------
        None
        '''
        save_path, _ = QFileDialog.getSaveFileName(self, "Export result text",
                                                   "Analysis_results.txt",
                                                   "Text Files, (*.txt)")

        if save_path:
            open_save_files.save_txt_to_file(save_path, self.resultsbox.toPlainText())

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
        labeled_image, self.results = segmentation_regions.find_regions(ondisplay, self.conf)

        ##Update plots
        self.region_plot.display_data(labeled_image, cmap='gray', clear=True)


        self.indiv_region_plot.display_data(self.data_from_zoom_window, cmap='gray', clear=True)
        self.indiv_region_plot.draw_single_region(properties=self.results)
        self.indiv_region_plot.regioncounter.setMinimum(1)
        self.indiv_region_plot.regioncounter.setMaximum(len(self.results['area']))

        self.region_plot.display_data(self.results, datatype='scatter')
        self.region_plot.display_data(self.results, datatype='regions')
        self.region_hist.display_data(self.results['area'], datatype='hist',clear=True)

        ##Text to result box
        txt = 'Region identification (look at corresponfing panel):\n'
        txt += f"Ratio of black regions [%]: {100*self.results['black_ratio']}\n"
        txt += f"Ratio of white regions [%]: {100*self.results['white_ratio']}\n"
        txt += f"Number of regions identified: {len(self.results['area'])}\n"
        txt += f"Smallest region: {min(self.results['area'])} pixels\n"
        txt += f"Largest region: {max(self.results['area'])} pixels"
        self.write_to_result_box(txt)

class Plot(QTabWidget):
    '''
    This class codes a simple panel with a plot inside
    '''
    def __init__(self, explorer=False, allregions=False, results_box_write=False,\
                 conversion=False):
        '''
        Class initialization
        Paramaeters
        -----------
        explorer:   bool
                    if True, some more widget are displayed for
                    individual region exploration

        allregions: bool
                    if True, some more widgets are displayed
                    for allregion plots

        results_box:    method (function)
                        the method to write in the result box
        '''
        ###create the tab
        QTabWidget.__init__(self)

        ##Make the grid
        grid = QGridLayout()
        self.setLayout(grid)

        ###Add the plot
        self.plot, self.fig, self.axs, self.toolbar = plots.create_plot(toolbar=True, transparent=True)
        self.axs.axis('off')
        grid.addWidget(self.plot, 0, 0, 7, 8)
        grid.addWidget(self.toolbar, 7, 0, 1, 5)

        ##results box writing
        if results_box_write is not False:
            self.results_box_write = results_box_write

        ##if explorer, we had a few widgets
        if explorer is True:
            ##Conversion pix_to_mm area
            self.conversion = conversion
            ##widgets
            grid.addWidget(QLabel('Choose region:'), 7, 6, 1, 1)
            self.regioncounter = QSpinBox()
            grid.addWidget(self.regioncounter, 7, 7, 1, 1)
            self.print_properties = QPushButton('Print region prop')
            grid.addWidget(self.print_properties, 7, 5, 1, 1)

            ###events
            self.regioncounter.valueChanged.connect(self.draw_single_region)
            self.print_properties.clicked.connect(self.write_to_box_in_analysis_window)

        elif allregions is True:
            ##Conversion pix_to_mm area
            self.conversion = conversion
            ##widgets
            self.save_properties = QPushButton('Save all regions properties')
            grid.addWidget(self.save_properties, 7, 7, 1, 1)
            self.save_properties.clicked.connect(self.save_properties_to_text)

    def display_data(self, data=None, cmap=None, datatype='image', clear=False):
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
        ###do we clear?
        if clear is True:
            ##clear the plot
            self.fig.clf()
            self.axs = self.fig.add_subplot()

            ###remove the previous patch and center
            if hasattr(self, 'region_indiv'):
                del self.region_indiv
                del self.region_center

        ###Display
        if datatype == 'image':
            self.ondisplay = self.axs.imshow(data, cmap=cmap)

            ###Remove axis
            self.axs.axes.set_axis_off()

        elif datatype == 'hist':
            ###Add hist
            self.axs.hist(data, bins=1000)
            self.axs.set_xlim(-5, numpy.median(data)+100*numpy.median(data))
            self.axs.set_xlabel('Size [pixels]')
            self.axs.set_ylabel('N')

            ###Remove axis
            self.axs.axes.set_axis_on()

        elif datatype == 'regions':
            self.add_regions(data)

        elif datatype == 'scatter':
            ##Add scatter plot
            self.axs.scatter(data['y'], data['x'], color='r',
                             marker='x', facecolors='none')

        ##Draw and adjust layout
        self.plot.draw()
        self.fig.tight_layout()

    def add_regions(self, regions):
        '''
        This method adds segmented regions as
        rectangles

        Parameters
        ----------
        regions     : dict
                      with region information

        Return
        ------
        None
        '''
        ##make the region an attribute
        self.results = regions

        ##Loop over the region
        for region in self.results['bbox']:
            ##get the box limits
            min_row, min_col, max_row, max_col = region
            ##Define the rectanle
            rect = patches.Rectangle((min_col, min_row), max_col-min_col,
                                     max_row - min_row,
                                     linewidth=1,
                                     edgecolor='y',
                                     facecolor='none')
            ##And draw it
            self.axs.add_patch(rect)

    def draw_single_region(self, properties = None):
        '''
        This draws a single region on the plot
        if one is already there, we remove it before
        the new one is identified

        Parameters
        ----------
        region_number   : int
                          label of the region

        properties      :  dict
                           with all regions properties

        Return
        ------
        None
        '''
        ###remove the previous patch and center
        if hasattr(self, 'region_indiv'):
            self.region_indiv.remove()
            self.region_center.remove()

        ###if no results where passed before we made them an attribute
        if not hasattr(self, 'results'):
            self.results = properties

        if hasattr(self, 'results') and properties is not None:

            ##region number
            region_number = self.regioncounter.value()

            ##Get region bbox
            min_row, min_col, max_row, max_col = self.results['bbox'][region_number-1]
            center_x = self.results['x'][region_number-1]
            center_y = self.results['y'][region_number-1]

            ##Create the rectangle
            self.region_indiv = patches.Rectangle((min_col, min_row), max_col-min_col,
                                                  max_row - min_row,
                                                  linewidth=2,
                                                  edgecolor='y',
                                                  facecolor='none')
            ##And draw it
            self.axs.add_patch(self.region_indiv)

            ##ANd the center
            self.region_center = self.axs.scatter([center_y], [center_x],
                                                  color='y', marker='x')

            ##Draw and adjust layout
            self.plot.draw()
            self.fig.tight_layout()

    def write_to_box_in_analysis_window(self):
        '''
        This method uses the function passed as argument 
        to write in the parent window textbox
        '''
        ##region counter and extract properties
        region_number = self.regioncounter.value()
        min_row, min_col, max_row, max_col = self.results['bbox'][region_number-1]
        area = self.results['area'][region_number-1]
        area_box = (max_col-min_col)*(max_row-min_row)

        ##Prepare text
        txt = f'Region #{region_number}:\n'
        txt += f"Area [#pixels] = {int(area)}\n"
        txt += f"Area [mm2] = {self.conversion * int(area)}\n"
        txt += f"Area_box [#pixels] = {int(area_box)}\n"
        txt += f"Area_box [mm2] = {self.conversion * int(area_box)}\n"
        self.results_box_write(txt)

    def save_properties_to_text(self):
        '''
        Save all the properties in a txt file

        Parameters
        ----------
        None
        
        Return
        ------
        None
        '''
        ##Prepare catalog
        txt = '#x\ty\tarea[pixels]\tarea[mm2]\n'

        for i,x in enumerate(self.results['x']):
            line = f"{self.results['x'][i]}\t{self.results['y'][i]}"
            line += f"\t{int(self.results['area'][i])}"
            line += f"\t{self.conversion*self.results['area'][i]}\n"
            txt += line

        save_path, _ = QFileDialog.getSaveFileName(self, "Export region catalog",
                                                   "Catalog.txt",
                                                   "Text Files, (*.txt)")

        if save_path:
            open_save_files.save_txt_to_file(save_path, txt)
