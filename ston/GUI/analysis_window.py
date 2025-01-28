"""
This file is part of the STON project (P.I. E. Dammer)
It creates the image analysis window

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""

####Standard Library

####python third party
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPlainTextEdit,\
                              QPushButton

####Local imports
from . import plots

class AnalysisWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, config):
        '''
        Class constructor
        '''
        super().__init__()
        self.hidden = True
        self.move(200,200)
        self.conf = config
        self.resize(self.conf['Conf']['zoom_window_width'],
                    self.conf['Conf']['zoom_window_height'])
        self.setWindowTitle('STON: Analysis window')

        ##Make the layout
        self.make_layout()

    def make_layout(self):
        '''
        Add widget to the window
        '''
        grid = QGridLayout()
        self.setLayout(grid)

        ##Plot
        self.plot, self.fig, self.axs, self.toolbar = plots.create_plot(toolbar=True)
        grid.addWidget(self.plot, 0, 0, 7, 8)
        grid.addWidget(self.toolbar, 7, 0, 1, 2)

        ##Result box
        grid.addWidget(QLabel('Resuls (read-only):'), 0, 9, 1, 1)
        self.results = QPlainTextEdit()
        self.results.setReadOnly(True)
        self.results.setFixedWidth(250)
        grid.addWidget(self.results, 1, 9, 6, 1)

        ###save image button
        save_image_button = QPushButton('Save image')
        grid.addWidget(save_image_button, 7, 9, 1, 1)
