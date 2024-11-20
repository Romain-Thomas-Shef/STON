"""
This file is part of the STON project (P.I. E. Dammer)
It creates the cluster window


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
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QGridLayout,\
                              QScrollArea, QHBoxLayout, QListView, QAbstractItemView,\
                              QApplication


####local impors
from . import image_processing

class ClusterWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, config, images_with_path, images_without_path, zoom_window):
        super().__init__()

        ###setup
        self.resize(config['Conf']['cluster_window_width'], config['Conf']['cluster_window_height'])
        self.move(400,400)
        self.setWindowTitle('STON: Cluster window')

        ##attributes
        self.images_with_path, self.images_without_path = images_with_path, images_without_path
        self.conf = config
        self.files_dict = self.conf['files_dict']
        self.zoom_window = zoom_window
        self.parent()

        ##Make the widgets
        self.make_layout()

    def make_layout(self):
        '''
        This method creates all the widget

        Parameters
        ----------
        None

        Return
        ------
        None
        '''
        ###create the grid
        grid = QGridLayout()
        self.setLayout(grid)
        row = 0

        ###set the srcolling area
        scroll = QScrollArea()
        self.scrollayout = QHBoxLayout()
        scrollwidget = QWidget()
        scrollwidget.setLayout(self.scrollayout)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollwidget)
        grid.addWidget(scroll, row, 0, 1, 4)

        ####place where image will be displayed
        self.image_list = QListWidget(
            viewMode=QListView.ViewMode.IconMode,
            iconSize= self.conf['Options']['Image_width'] * QtCore.QSize(1, 1),
            resizeMode=QListView.ResizeMode.Adjust)
        self.image_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        #self.image_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.scrollayout.addWidget(self.image_list)
        row += 1

        ###load the images
        self.load_images()

        ##connect events
        self.image_list.itemDoubleClicked.connect(self.send_to_zoom)

    def load_images(self):
        '''
        Load the images
        '''
        ###Start displaying
        for name,nameandpath in zip(self.images_without_path, self.images_with_path):
            ##Create and Widget item with the file name
            ##it will go below the image
            newitem = QListWidgetItem(name)

            ##process image
            data, image = \
                image_processing.make_thumbnail_from_image(nameandpath,
                                                           self.conf['Options']['Downgrade_factor'])
            ##create the icon
            item_with_icon = image_processing.create_icon(data, image, newitem)

            ##and add it to the display area
            self.image_list.addItem(item_with_icon)

            ###Process the event
            QApplication.processEvents()

    def send_to_zoom(self):
        '''
        This method sends the selected image(s) to the second window for inspection
        '''
        ###get all selected images
        listitems=self.image_list.selectedItems()

        ###if some items are selected we remove them
        image_name = listitems[0].text()
        for folder in self.files_dict:
            if os.path.basename(folder) != image_name:
                for files in self.files_dict[folder]:
                    if files == image_name:
                        filepath = os.path.join(folder, image_name)

        ###send to zoom window
        self.zoom_window.change_image(filepath)
