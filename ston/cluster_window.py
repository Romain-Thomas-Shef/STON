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
from PySide6.QtWidgets import QWidget


####local impors
from . import image_processing

class ClusterWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, config, images_with_path, images_without_path):
        super().__init__()

        ###
        self.resize(config['Conf']['cluster_window_width'], config['Conf']['cluster_window_height'])
        self.move(400,400)
        self.setWindowTitle('STON: Cluster window')
        self.parent()
