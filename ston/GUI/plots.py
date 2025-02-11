"""
This file is part of the STON project (P.I. E. Dammer)
It creates a plot to be embedded within a window
It also customizes slightly the toolbar

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
    This creates the plot.
    
    Parameters
    ----------
    toolbar     :   Bool
                    if use a toolbar. by default is false

    Return
    ------
    canvas      : FigureCanvasQT
                  area onto which the figure is drawn
    fig         : Figure
                  where the axes are drawn
    axs         : Axes
                  the actual plot
    toolbar     : NavigationToolbar2QT
                  the toolbar
    '''
    #Create a matplotlib figure and axes instance, with the plotting parameters
    fig, axs = plt.subplots(1, 1, dpi=100)

    #Create the Matplotlib canvas widget, and add to parent layout
    canvas = FigureCanvas(fig)

    ##if we use a toolbar
    if toolbar:
        toolbar = NavigationToolbarCustom(canvas)
    else:
        toolbar = None

    #Some widget resizing code, not sure what it does but was in a tutorial... TO be removed?
    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    canvas.updateGeometry()

    return canvas, fig, axs, toolbar


class NavigationToolbarCustom(NavigationToolbar):
    '''
    This class creates a custom toolbar
    '''
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Customize', 'Save')]
