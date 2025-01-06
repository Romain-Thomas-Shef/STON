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
from functools import partial

####python third party
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QGridLayout,\
                              QScrollArea, QHBoxLayout, QListView, QAbstractItemView,\
                              QApplication, QPushButton, QDialog, QDialogButtonBox,\
                              QLabel, QComboBox, QLineEdit, QFileDialog

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

        ###add button for mashup
        mashup = QPushButton('Create Mash-up')
        grid.addWidget(mashup, row, 0, 1, 1)

        ###add button to create a list with file names of image clusters
        export_button = QPushButton('Export Cluster List')
        grid.addWidget(export_button, row, 1, 1, 1)
        
        ###load the images
        self.load_images()

        ##connect events
        self.image_list.itemDoubleClicked.connect(self.send_to_zoom)
        mashup.clicked.connect(self.mashup_dialog)
        export_button.clicked.connect(self.export_cluster_list)

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

    def export_cluster_list(self):
        ''' 
        Save names of all clustered images to a text file
        '''
        save_path, _ = QFileDialog.getSaveFileName(self, "Export Cluster List", "new_cluster_list.txt", "Text Files, (*.txt)")
        if save_path:
            with open(save_path, 'w') as file:
                for image_index in range(self.image_list.count()):
                    file.write(self.image_list.item(image_index).text() + '\n'
            print(f"File names saved to {save_path}")
            

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

    def mashup_dialog(self):
        '''
        This method get all the images (selected OR not) that are displayed
        in the image list
        '''

        ###get all images
        filelist = []
        for image_index in range(self.image_list.count()):
            filelist.append(self.image_list.item(image_index).text())

        ##dialog
        dialog = MashupDialog(filelist, self.conf['Project_info']['Directory'])
        if dialog.exec():
            ###if the user clicked 'ok' on the mashup dialog we retrieve the configuration and
            ###send it to the mashup maker
            configmashup = dialog.get_mashup_config()
            final_image = image_processing.make_mashup(configmashup, self.images_with_path)
            self.zoom_window.change_image(final_image)

        else:
            ####if the user clicked on 'cancel', or pressed escape
            print("Cancel!")


class MashupDialog(QDialog):
    '''
    This class inherits from QDialog and creates the mashup Dialog
    It gives the options for sorting the files in the mashup and
    select a direction
    '''
    def __init__(self, filelist, directory):
        super().__init__()

        self.setWindowTitle("Mashup")

        ###attribute
        self.filelist = filelist


        ###create widgets
        layout = QGridLayout()
        row = 0

        ##name of the mashup
        self.name = QLineEdit('name.jpg')
        layout.addWidget(self.name, row, 0, 1, 1)
        savebutton = QPushButton('Choose File')
        layout.addWidget(savebutton, row, 1, 1, 1)
        row += 1

        ###order of the mashup
        message = QLabel("Select order:")
        layout.addWidget(message, row, 0, 1, 1)
        row += 1

        #we create the combobox programitically
        for image in self.filelist:
            ###create comboboxes and Qlabel dynamically
            setattr(self, f'CB_{image}', QComboBox())

            ###add filename
            image_name = QLabel(image)
            layout.addWidget(image_name, row, 0, 1, 1)

            ##add number to comboboxes
            combobox = getattr(self, f'CB_{image}')
            for n in range(len(self.filelist)):
                combobox.addItem(str(n+1))
            layout.addWidget(combobox, row, 1, 1, 1)

            row += 1

        ###ok/cancel buttons
        qbutton = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonbox = QDialogButtonBox(qbutton)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        layout.addWidget(self.buttonbox, row, 0, 1, 1)


        ##save button dialog
        savebutton.clicked.connect(partial(self.savefile, directory))


        self.setLayout(layout)

    def savefile(self, directory):
        '''
        This method open a file dialog for saving a file

        Parameters
        ----------
        directory   str
                    project directory

        Return
        ------
        None
        '''
        filename, _ = QFileDialog.getSaveFileName(caption='Save File', dir=directory)
        self.name.setText(filename)

    def get_mashup_config(self):
        '''
        This method analysis the state of all widget and create a configuration
        dictionary
        '''

        ##initialize a dictionary
        config = {}

        ###name of the mashup
        config['name'] = self.name.text()

        ##get all widgets for order
        for image in self.filelist:
            dropdown = getattr(self, f'CB_{image}')
            config[image] = int(dropdown.currentText())

        return config
