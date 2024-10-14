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
from PyQt6.QtWidgets import QMainWindow, QSplitter, QWidget, QGridLayout, QStatusBar,\
                            QTreeWidget, QTreeWidgetItem, QToolBar
from PyQt6 import QtGui, QtCore

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

        ##font
        self.font = 'medium'

        ##populate with widget
        self.make_layout()

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
        #dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        #logo = os.path.join(dir_path, 'docts/source/images/logo/favison.ico')
        #self.setWindowIcon(QtGui.QIcon(logo))

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
        grid = QGridLayout()
        left.setLayout(grid)
        left.setFixedWidth(400)
        row = 0
        
        ###create the tree
        self.tree = QTreeWidget()
        grid.addWidget(self.tree)

        

        ####right part
        right = QWidget()
        right_grid = QGridLayout()
        right.setLayout(grid)

        ###add everything to the split
        split.addWidget(left)
        split.addWidget(right)

        ####connect every button to functions

        ###status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
