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
                            QListWidgetItem, QPushButton, QVBoxLayout, QApplication,\
                            QFileDialog


####local impors
from . import explore_files
from . import zoom_window
from . import cluster_window
from . import comparison_window
from . import image_processing
from . import conf

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

        ##get all files
        self.files_dict = explore_files.get_dir_and_files(self.conf['Project_info']['Directory'],\
                                                          self.conf['Options']['Extensions'])

        ###set the size and title of the window
        self.resize(self.conf['Conf']['main_window_width'], self.conf['Conf']['main_window_height'])
        self.setWindowTitle('STON: SofTware for petrOgraphic visualisatioN'+
                            f" - {self.conf['Project_info']['Name']} - By R. Thomas and E. Dammer")

        ###add the logo
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.logo = os.path.join(dir_path, 'docs/source/images/logo/logo.jpeg')
        self.setWindowIcon(QtGui.QIcon(self.logo))

        ###cluster window counter
        self.n_cluster = 1

        ###Comparison window counter
        self.n_comparison = 1

        ##populate with widget
        self.make_layout()

        ###and display it
        self.show()

        ###create detail window (hidden)
        self.zoom_window = zoom_window.DetailWindow(self.logo, self.conf)

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

        ##Load conf button
        button_load = QPushButton('Load new configuration')
        left_grid.addWidget(button_load, row, 0, 1, 2)
        row += 1

        ###create the tree
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Files"])
        ###populate
        self.populate_tree()

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

        ####image of the logo in the zoom area (just at the start of the GUI)
        self.zoom = QLabel()
        pixmap = QtGui.QPixmap(self.logo)
        scaled = pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom.setPixmap(scaled)
        left_grid.addWidget(self.zoom, row, 0, 5, 2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        row += 5

        ##zoom window button
        button_hide_zoom = QPushButton('Zoom window')
        left_grid.addWidget(button_hide_zoom, row, 0, 1, 1)

        ##remove button
        button_cluster = QPushButton('Cluster window')
        left_grid.addWidget(button_cluster, row, 1, 1, 1)
        row += 1

        ##compare window button
        button_compare = QPushButton('size by size comparison')
        left_grid.addWidget(button_compare, row, 0, 1, 2)
        row += 1

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
        #self.image_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
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
        button_hide_zoom.clicked.connect(self.hide_zoom_window)
        button_cluster.clicked.connect(self.open_cluster_window)
        button_compare.clicked.connect(self.open_compare_window)
        button_load.clicked.connect(self.get_new_conf)
        self.image_list.itemDoubleClicked.connect(self.send_to_zoom)
        self.tree.itemDoubleClicked.connect(self.loadimages)


    def populate_tree(self):
        '''
        This method populate the file tree with file name
        Parameter
        ---------
        None

        Return
        ------
        None
        '''

        ###remove any potential files that was there before
        self.tree.clear()

        ###and update with the new list
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

        date = str(datetime.datetime.now()).split('.', maxsplit=1)[0]
        if msgtype == 'startup':
            final_text = f"[{date}, -Startup] : " + text
            self.log.appendHtml(f'<span style="color:blue;">{final_text} </span>')

        if msgtype == 'Error':
            final_text = f"[{date}, -Error] : " + text
            self.log.appendHtml(f'<span style="color:red;">{final_text} </span>')

        if msgtype == 'Info':
            final_text = f"[{date}, -Info] : " + text
            self.log.appendHtml(f'<span style="color:green;">{final_text} </span>')

        if msgtype == 'Warning':
            final_text = f"[{date}, -Warning] : " + text
            self.log.appendHtml(f'<span style="color:orange;">{final_text} </span>')

        self.log.repaint()

    def loadimages(self):
        '''
        Method is selected whem the load button is pressed
        It checks that some items have been selected and, if
        this is the case load the images.
        '''
       	###Get the selected files in the tree
        listfiles = [file.text(0) for file in self.tree.selectedItems()]

        ##And get images that are already displayed
        listdisplayed = [self.image_list.item(x).text() for x in range(self.image_list.count())]

        if listfiles:
            ###Give info
            self.printinlog('Info', f'{len(listfiles)} items selected')
            self.printinlog('Info', 'Analyse selection...')

            ###assemble paths of selected objects
            images_with_path, images_without_path = \
                    explore_files.get_files_and_path(listfiles,
                                                     self.files_dict,
                                                     listdisplayed)

            ##if some files are images we display
            if not images_with_path:
                self.printinlog('Warning',
                                'No (new) images found in the selected files...try again')

            else:
                #give info
                self.printinlog('Info', f'{len(images_with_path)} image(s) selected')
                self.printinlog('Info', 'Start displaying...')

            	###Start displaying
                for name,nameandpath in zip(images_without_path, images_with_path):

                    ##Create and Widget item with the file name
                    ##it will go below the image
                    newitem = QListWidgetItem(name)

                    ##process image
                    data, image = \
                       image_processing.make_thumbnail_from_image(nameandpath,
                                                                  self.conf['Options']['Downgrade_factor'])
                    ###convert to QImages and then Pixmap
                    qim = QtGui.QImage(data, image.size[0], image.size[1],
                                       QtGui.QImage.Format.Format_RGBA8888)
                    pix = QtGui.QPixmap.fromImage(qim)
                    ##Create the Icon
                    icon = QtGui.QIcon()
                    icon.addPixmap(pix)
                    newitem.setIcon(icon)

                    ###And add to the list and print in log
                    self.image_list.addItem(newitem)
                    self.printinlog('Info', f"{name} is displayed")

                    ###Process the event
                    QApplication.processEvents()
                    time.sleep(0.025)

        else:
            self.printinlog('Warning', 'No files selected')

    def remove_single_image(self):
        '''
        This method remove the selected image from the displayed area
        '''
        ###get all selected images
        listitems=self.image_list.selectedItems()

        ###if some items are selected we remove them
        for item in listitems:
            self.image_list.takeItem(self.image_list.row(item))
            image_name = item.text()
            self.printinlog('Warning', f'{image_name} was removed.')

    def remove_all_images(self):
        '''
        This method remove all the images from the displayed area
        '''
        self.image_list.clear()
        self.printinlog('Warning', 'Displayer has been cleared. No images are displayed.')


    def open_cluster_window(self):
        '''
        This method open the cluster window
        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        ###get all selected images
        listitems=self.image_list.selectedItems()

        ##And get images that are already displayed
        listdisplayed = [item.text() for item in listitems]

        ###assemble paths of selected objects
        images_with_path, \
                images_without_path = explore_files.get_files_and_path(listdisplayed,
                                                                       self.files_dict, [])

        ###if some files where found
        if images_with_path: #checks if something is selected
            ###create cluster window with a dynamic name
            setattr(self, f'Cluster_window_n{self.n_cluster}',
                    cluster_window.ClusterWindow(self.conf, images_with_path, images_without_path))
            ###extract it back
            window = getattr(self, f'Cluster_window_n{self.n_cluster}')
            ###display it
            window.show()
            ###increment the counter
            self.n_cluster += 1

        else:
            self.printinlog('Warning', 'No files were selected')


    def open_compare_window(self):
        '''
        This method open the comparison window
        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        ###get all selected images
        listitems=self.image_list.selectedItems()

        ##And get images that are already displayed
        listdisplayed = [item.text() for item in listitems]

        ###assemble paths of selected objects
        images_with_path,\
                images_without_path = explore_files.get_files_and_path(listdisplayed,
                                                                       self.files_dict, [])

        ###if some files where found
        if len(images_with_path) == 2: #checks if two images where selected
            ###create cluster window with a dynamic name
            setattr(self, f'Comparison_window_n{self.n_comparison}',
                    comparison_window.CompareWindow(self.conf, images_with_path,\
                                                    images_without_path))
            ###extract it back
            window = getattr(self, f'Comparison_window_n{self.n_comparison}')
            ###display it
            window.show()
            ###increment the counter
            self.n_comparison += 1

            ##and print in log
            self.printinlog('Info', 'Selected images have been opened in comparison window.')

        elif len(images_with_path) > 2:
            self.printinlog('Error', 'You selected more than two images. The comparison window only work with two. Try again.')

        else:
            self.printinlog('Error', 'Not enough files were selected. Two are needed. Try again')




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

    def get_new_conf(self):
        '''
        This method is triggered when the use wants to change the configuration file
        It opens a dialog to find a new file

        Parameter
        ---------
        None

        Return
        ------
        None
        '''
        ##create the dialog file
        selected_file = QFileDialog.getOpenFileName(parent=self, caption='select',
                                           options=QFileDialog.DontUseNativeDialog)

        ##get the file
        file = selected_file[0]
        if not file:
            self.printinlog('Error', 'No file selected, try again')
        else:
            self.printinlog('Warning', f'Attempt to load configuation from {file}')
            try:
                ###load conf
                configuration, _ = conf.load_conf(file, self.conf['Conf']['OS'])
                self.conf = configuration

                ###clear displayer
                self.remove_all_images()

                ##update the files dict
                self.files_dict = \
                        explore_files.get_dir_and_files(self.conf['Project_info']['Directory'],\
                                                        self.conf['Options']['Extensions'])

                ##and repopulate the file tree
                self.populate_tree()

                ###and update the image size in the displayer area
                self.image_list.setIconSize(self.conf['Options']['Image_width'] * \
                                            QtCore.QSize(1, 1))

                self.printinlog('Info', f'Configuration from {file} loaded')

            except:
                self.printinlog('Error', f'Could not read configuration from {file}')



    def closeevent(self, event):
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
