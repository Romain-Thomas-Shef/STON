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

####python third party
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QSplitter, QWidget, QGridLayout, QStatusBar,\
                            QTreeView, QTreeWidgetItem, QToolBar, QTabWidget,\
                            QLabel

####local impors
from . import explore_files


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
        self.configuration = configuration

        ###selected lines attributes
        self.selected_lines = []
        self.displayed_lines = []

        ##get all files
        files_dict = explore_files.get_dir_and_files(self.configuration['Project_directory'],
                                                     self.configuration['With_hidden'])


        ###set the size and title of the window
        self.resize(self.configuration['Window-width'], self.configuration['Window-height'])
        self.setWindowTitle('STON: SofTware for petrOgraphic visualisatioN'+
                            f" - {self.configuration['Project_name']}")

        ###add toolbar
        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.addToolBar(self.toolbar)
        #Toolbar_setup(self.toolbar) ##--> https://www.pythonguis.com/tutorials/pyqt6-actions-toolbars-menus/

        ###add the logo
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.logo = os.path.join(dir_path, 'docs/source/images/logo/logo.jpeg')
        self.setWindowIcon(QtGui.QIcon(self.logo))

        ##populate with widget
        self.make_layout()

        ###and display it
        self.show()


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
        #left.setFixedWidth(400)
        row = 0
        
        ###create the tree
        self.tree = QTreeView()
        self.model = QtGui.QFileSystemModel()
        self.model.setNameFilters(self.configuration['Extensions'])
        self.model.setNameFilterDisables(False)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(str(self.configuration['Project_directory'])))
        self.model.setRootPath(str(self.configuration['Project_directory']))
        self.tree.setFixedWidth(400)
        left_grid.addWidget(self.tree, row, 0, 15, 1)
        row += 15

        ###Selected image label
        self.label = QLabel('Selected Image:')
        left_grid.addWidget(self.label, row, 0, 1, 1)
        row += 1

        ####image of the logo in the zoom area (just at the start of the GUI)
        self.zoom = QLabel()
        pixmap = QtGui.QPixmap(self.logo)
        scaled = pixmap.scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom.setPixmap(scaled)
        left_grid.addWidget(self.zoom, row, 0, 5, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        ###create the tab on the right
        self.right = QTabWidget()

        ###add everything to the split
        split.addWidget(left)
        split.addWidget(self.right)
        split.setStretchFactor(1, 10)

        ###status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
