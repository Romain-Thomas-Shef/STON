"""
This file is part of the STON project (P.I. E. Dammer)
It creates a plot in to be embedded within a window

Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
"""

####python third party
from PySide6.QtWidgets import QSizePolicy

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



def create_plot(toolbar=False):
    '''
    This initialize the image plot
    '''
    #Create a matplotliub figure and axes isntance, witth the plotting parameters
    fig, axs = plt.subplots(1, 1, dpi=100)

    #Create the Matplotlib canvas widget, and add to parent layout
    canvas = FigureCanvas(fig)

    ##if we use a toolbar
    if toolbar:
        toolbar = NavigationToolbar(canvas)
    else:
        toolbar = None

    #Some widget resizing code, not sure what it does but was in a tutorial... TO be removed?
    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    canvas.updateGeometry()

    return canvas, fig, axs, toolbar
