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
import os
import datetime
import time

####python third party
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QGridLayout,\
                            QTreeWidgetItem, QTabWidget, QLabel, QTreeWidget,\
                            QHeaderView, QAbstractItemView, QPlainTextEdit,\
                            QScrollArea, QHBoxLayout, QListView, QListWidget,\
                            QListWidgetItem, QPushButton, QVBoxLayout, QApplication

from PIL import Image


####local impors
from . import explore_files
from . import zoom_window

class ClusterWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, config):
        super().__init__()
        self.hidden = True
        self.resize(config['Conf']['Window-width']/2, config['Conf']['Window-height']/2)
        self.move(400,400)
        self.setWindowTitle('STON: Cluster window')
        self.parent()

class GUI(QMainWindow):
    '''
    This class defines the main window of scuba that we will populate
    with panels.
    '''

    def __init__(self, configuration):
        '''
        Initialization of the main panel
        Parameters
        ----------
        configuration   :   str
                            initial configuration of the tool

        Return
        ------
        None
        '''
        super().__init__()

        ###The configuration becomes an attribute
        self.conf = configuration

        ###selected lines attributes
        self.selected_lines = []
        self.displayed_lines = []
        self.target = None
        self.setAcceptDrops(True)

        ##get all files
        self.files_dict = explore_files.get_dir_and_files(self.conf['Project_info']['Directory'],\
                                                          self.conf['Options']['Extensions'])

        ###set the size and title of the window
        self.resize(self.conf['Conf']['Window-width'], self.conf['Conf']['Window-height'])
        self.setWindowTitle('STON: SofTware for petrOgraphic visualisatioN'+
                            f" - {self.conf['Project_info']['Name']} - By R. Thomas and E. Dammer")

        ###add the logo
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.logo = os.path.join(dir_path, 'docs/source/images/logo/logo.jpeg')
        self.setWindowIcon(QtGui.QIcon(self.logo))

        ##populate with widget
        self.make_layout()

        ###and display it
        self.show()

        ###create detail window (hidden)
        self.zoom_window = zoom_window.DetailWindow(self.logo)

        ###And cluster window (hidden)
        self.cluster_window = ClusterWindow(self.conf)

        ###Start up is done, give info in log
        self.printinlog('startup', 'Welcome to STON!')

    def make_layout(self):
        '''
        This method creates the layour of the window
        '''

        #create central widget
        split = QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.setCentralWidget(split)

        ####left part with widget
        left = QWidget()
        left_grid = QGridLayout()
        left.setLayout(left_grid)
        row = 0

        ##zoom window button
        button_hide_zoom = QPushButton('Zoom window')
        left_grid.addWidget(button_hide_zoom, row, 0, 1, 1)

        ##remove button
        button_hide_cluster = QPushButton('Cluster window')
        left_grid.addWidget(button_hide_cluster, row, 1, 1, 1)
        row += 1

        ###create the tree
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Files"])
        ###populate
        items = []
        for key, values in self.files_dict.items():
            item = QTreeWidgetItem([os.path.basename(key)])
            for value in values:
                ext = value.split(".")[-1].upper()
                child = QTreeWidgetItem([value, ext])
                item.addChild(child)
            items.append(item)
        self.tree.insertTopLevelItems(0, items)
        ###Adjust some propertiess
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        ###add it to the grid
        left_grid.addWidget(self.tree, row, 0, 15, 2)
        row += 15

        ##Load button
        button = QPushButton('Load selected Image(s)')
        left_grid.addWidget(button, row, 0, 1, 2)
        row += 1

        ##Clear selection
        button_clear = QPushButton('Clear displayer')
        left_grid.addWidget(button_clear, row, 0, 1, 1)

        ##remove button
        button_remove = QPushButton('Remove selected Image')
        left_grid.addWidget(button_remove, row, 1, 1, 1)
        row += 1

        ##remove button
        button_inspect = QPushButton('Inspect selected Image(s)')
        left_grid.addWidget(button_inspect, row, 0, 1, 2)
        row += 1

        ####image of the logo in the zoom area (just at the start of the GUI)
        self.zoom = QLabel()
        pixmap = QtGui.QPixmap(self.logo)
        scaled = pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom.setPixmap(scaled)
        left_grid.addWidget(self.zoom, row, 0, 5, 2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        ###create the tab on the right
        self.right = QTabWidget()
        hbox = QVBoxLayout()
        self.right.setLayout(hbox)

        ###set the srcrlling area
        scroll = QScrollArea()
        self.scrollayout = QHBoxLayout()
        scrollwidget = QWidget()
        scrollwidget.setLayout(self.scrollayout)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollwidget)
        hbox.addWidget(scroll)

        ####place where image will be displayed
        self.image_list = QListWidget(
            viewMode=QListView.ViewMode.IconMode,
            iconSize= self.conf['Options']['Image_width'] * QtCore.QSize(1, 1),
            resizeMode=QListView.ResizeMode.Adjust)
        self.image_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.scrollayout.addWidget(self.image_list)

        ##Add log window
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(150)
        hbox.addWidget(self.log)

        ###add everything to the split
        split.addWidget(left)
        split.addWidget(self.right)
        split.setStretchFactor(1, 10)

        ####Connect events
        button.clicked.connect(self.loadimages)
        button_remove.clicked.connect(self.remove_single_image)
        button_clear.clicked.connect(self.remove_all_images)
        button_inspect.clicked.connect(self.inspect)
        button_hide_zoom.clicked.connect(self.hide_zoom_window)
        button_hide_cluster.clicked.connect(self.hide_cluster_window)
        self.image_list.itemDoubleClicked.connect(self.send_to_zoom)

    def printinlog(self, msgtype, text):
        '''
        Prints images in log window
        Parameters
        ----------
        msgtype :	str
                        type of message
        text    :       str
                        text to display
         
        Return:
        ------
        None
        '''

        if msgtype == 'startup':
            final_text = f"[{str(datetime.datetime.now()).split('.')[0]}, Startup] : " + text
            self.log.appendHtml(f'<span style="color:blue;">{final_text} </span>')

        if msgtype == 'Error':
            final_text = f"[{str(datetime.datetime.now()).split('.')[0]}, --Error] : "  + text
            self.log.appendHtml(f'<span style="color:red;">{final_text} </span>')

        if msgtype == 'Info':
            final_text = f"[{str(datetime.datetime.now()).split('.')[0]}, ---Info] : "  + text
            self.log.appendHtml(f'<span style="color:green;">{final_text} </span>')

        if msgtype == 'Warning':
            final_text = f"[{str(datetime.datetime.now()).split('.')[0]}, Warning] : " + text
            self.log.appendHtml(f'<span style="color:orange;">{final_text} </span>')

        self.log.repaint()

    def loadimages(self):
        '''
        Method is selected whem the load button is pressed
        It checks that some items have been selected and, if
        this is the case load the images.
        '''
       	###Get the selected images in the tree
        listimage = self.tree.selectedItems()

        ##And get images that are already displayed
        listitems = [self.image_list.item(x).text() for x in range(self.image_list.count())]

        if listimage:
            ###Give info
            self.printinlog('Info', f'{len(listimage)} items selected')
            self.printinlog('Info', 'Analyse selection...')

            ##Start checking selected images
            goodimages = 0
            goodimages_with_path = []
            goodimages_without_path = []
            ##go over all imtes
            for item in listimage:
                ##Get the image name
                name = item.text(0)  ###-->column 0 of the tree

                ##If the image is already displayed then we stop the loop  
                if name in listitems:
                    self.printinlog('Warning', f'{name} already displayed')
                    continue
                
                ###Check if this are file names (and not directory)
                for folder in self.files_dict:
                    if os.path.basename(folder) != name:
                        for files in self.files_dict[folder]:
                            if files == name and name not in goodimages_without_path:
                                goodimages += 1
                                goodimages_with_path.append(os.path.join(folder,name))
                                goodimages_without_path.append(name)


            ##if some files are images we display
            if not goodimages_with_path:
                self.printinlog('Warning', 'No (new) images found in the selected file...try again')

            else:
                #give info
                self.printinlog('Info', f'{len(goodimages_with_path)} were selected')
                self.printinlog('Info', 'Start displaying...')

            	###Start displaying
                for file in goodimages_with_path:

                    ##Get name to display below the thumbnail
                    name = os.path.basename(file)
                    it = QListWidgetItem(name)

                    ##open image
                    image = Image.open(file)

                    ###Reduce size (no need to have full resolution for the list of image)
                    im = image.thumbnail((image.size[1]/5,image.size[0]/5))
                    im = image.convert("RGBA")
                    data = im.tobytes("raw","RGBA")

                    ###convert to QImages and then Pixmap
                    qim = QtGui.QImage(data, im.size[0], im.size[1],
                                       QtGui.QImage.Format.Format_RGBA8888)
                    pix = QtGui.QPixmap.fromImage(qim)

                    ##Create the Icon
                    icon = QtGui.QIcon()
                    icon.addPixmap(pix)
                    it.setIcon(icon)

                    ###And add to the list
                    self.image_list.addItem(it)

                    ###Process the event
                    QApplication.processEvents()
                    time.sleep(0.05)

        else:
            self.printinlog('Warning', 'No files selected')

    def remove_single_image(self):
        '''
        This method remove the selected image from the displayed area
        '''
        ###get all selected images
        listItems=self.image_list.selectedItems()

        ###if some items are selected we remove them
        for item in listItems:
            self.image_list.takeItem(self.image_list.row(item))
            image_name = item.text()
            self.printinlog('Warning', f'{image_name} was removed.')

    def remove_all_images(self):
        '''
        This method remove all the images from the displayed area
        '''
        self.image_list.clear()
        self.printinlog('Warning', 'Displayer has been cleared. No images are displayed.')


    def inspect(self):
        '''
        This method sends the selected image(s) to the second window for inspection
        '''
        ###get all selected images
        listItems=self.image_list.selectedItems()

        ###if some items are selected we remove them
        if listItems:
            all_selected_images = []
            for item in listItems:
                ####give info
                self.printinlog('Info', 'Start inspection.')
                ##get image name
                image_name = item.text()
                ##assemble path
                for folder in self.files_dict:
                    if os.path.basename(folder) != image_name:
                        for files in self.files_dict[folder]:
                            if files == image_name:
                                all_selected_images.append(os.path.join(folder, image_name))

            ###And send them all to the seond window

        else:
            self.printinlog('Warning', 'No Image(s) selected for inspection')

    def hide_zoom_window(self):
        '''
        This method show/hide the zoom window
        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.zoom_window.hidden:
            self.zoom_window.show()
            self.zoom_window.hidden = False
        else:
            self.zoom_window.hide()
            self.zoom_window.hidden = True

    def hide_cluster_window(self):
        '''
        This method show/hide the cluster window
        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.cluster_window.hidden:
            self.cluster_window.show()
            self.cluster_window.hidden = False
        else:
            self.cluster_window.hide()
            self.cluster_window.hidden = True

    def send_to_zoom(self):
        '''
        This method sends the selected image(s) to the second window for inspection
        '''
        ###get all selected images
        listItems=self.image_list.selectedItems()

        ###if some items are selected we remove them
        image_name = listItems[0].text()
        for folder in self.files_dict:
            if os.path.basename(folder) != image_name:
                for files in self.files_dict[folder]:
                    if files == image_name:
                        filepath = os.path.join(folder, image_name)
        if filepath:
            self.zoom_window.change_image(filepath)
        else:
            self.printinlog('Error', 'File not found..')


    def closeEvent(self, event):
        '''
        This method makes sure that when them ain window is closed all
        the other windows are closed too
        Parameters
        ----------
        event   :   QEvent
                     
        Return
        ------
        None
        '''
        QApplication.closeAllWindows()
        event.accept()
