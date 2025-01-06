"""
This file is part of the STON project (P.I. E. Dammer)
It creates a personal slider setup

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""

####Standard Library

####python third party
from PySide6 import QtCore
from PySide6.QtWidgets import QSlider

####local impors

class Slider(QSlider):
    '''
    This class is inheriting from the QSlider widget
    and set up some common properties
    '''
    def __init__(self):
        '''
        This is the class constructor
        '''
        super().__init__()
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setMinimum(0)
        self.setMaximum(500)
        self.setValue(100)
