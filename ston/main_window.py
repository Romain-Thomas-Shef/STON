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
import random #temp

####python third party
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QSplitter, QWidget, QGridLayout, QStatusBar,\
                            QTreeView, QTreeWidgetItem, QToolBar, QTabWidget,\
                            QLabel, QTreeWidget, QHeaderView, QAbstractItemView,\
                            QPlainTextEdit, QScrollArea, QHBoxLayout, QTableWidget,\
                            QListView, QListWidget, QListWidgetItem

####local impors
from . import explore_files

class tree(QTreeWidget):
    '''
    We subclass the tree widget to change
    mimeData for the draganddrop events
    '''
    def __init__(self):
        '''
        Class constructor
        '''
        super().__init__()

    def mimeData(self, items):
        '''
        Change the mime data to add the text
        '''
        md = super().mimeData(items)
        text = "|".join([it.text(0) for it in items])
        md.setText(text)
        return md



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
                            f" - {self.conf['Project_info']['Name']}")

        ###add toolbar
        #self.toolbar = QToolBar("My main toolbar")
        #self.toolbar.setIconSize(QtCore.QSize(16, 16))
        #self.addToolBar(self.toolbar)
        #Toolbar_setup(self.toolbar) ##--> https://www.pythonguis.com/tutorials/pyqt6-actions-toolbars-menus/

        ###add the logo
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.logo = os.path.join(dir_path, 'docs/source/images/logo/logo.jpeg')
        self.setWindowIcon(QtGui.QIcon(self.logo))

        ##populate with widget
        self.filenames_iterator = None
        self.timer_loading = QtCore.QTimer(interval=20, timeout=self.load_image)
        self.make_layout()
    
        self.eventTrap = None

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
        row = 0
        
        ###create the tree
        self.tree = tree()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Directory", "Name"])
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
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.tree.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        ###add it to the grid
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
        hbox = QHBoxLayout()
        self.right.setLayout(hbox)

        ###set the srcrlling area
        scroll = QScrollArea()
        self.scrollayout = QHBoxLayout()
        scrollwidget = QWidget()
        scrollwidget.setLayout(self.scrollayout)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollwidget)
        hbox.addWidget(scroll)
        edit = PT()
        edit.setFixedWidth(200)
        self.scrollayout.addWidget(edit)

	####place where image will be displayed
        self.image_list = QListWidget(
            viewMode=QListView.ViewMode.IconMode,
            iconSize= self.conf['Options']['Image_width'] * QtCore.QSize(1, 1),
            resizeMode=QListView.ResizeMode.Adjust,
        )
        self.image_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.scrollayout.addWidget(self.image_list)
        self.start_loading(self.conf['Project_info']['Directory'])

        ###add everything to the split
        split.addWidget(left)
        split.addWidget(self.right)
        split.setStretchFactor(1, 10)

        ###status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def start_loading(self, directory):
        if self.timer_loading.isActive():
            self.timer_loading.stop()
        self.filenames_iterator = self.load_images(directory)
        print(directory)
        self.image_list.clear()
        self.timer_loading.start()


    def load_image(self):
        try:
            filename = next(self.filenames_iterator)
        except StopIteration:
            self.timer_loading.stop()
        else:
            name = os.path.basename(filename)
            print(name)
            it = QListWidgetItem(name)
            it.setIcon(QtGui.QIcon(filename))
            self.image_list.addItem(it)

    def load_images(self, directory):
        it = QtCore.QDirIterator(
            directory,
            ["*.tif", "*.png"],
            QtCore.QDir.Filter.Files)
        while it.hasNext():
            filename = it.next()
            print(filename)
            yield filename


class MydraggableGrid(QTableWidget):
    def __init__(self, columns, rows):
        super().__init__()
        #self.eventTrap = None
        #self.target = None
        self.setRowCount(int(rows))
        self.setColumnCount(int(columns))
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def eventFilter(self, watched, event:QtCore.QEvent):
        '''
        This method implements an mouse event filter
        '''
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            #self.mousePressEvent(event)
            print('press')
        elif event.type() == QtCore.QEvent.Type.MouseMove:
            #self.mouseMoveEvent(event)
            print('move')
        elif event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            #self.mouseReleaseEvent(event)
            print('release')
        return super().eventFilter(watched, event)

    '''
    def get_index(self, pos) -> int:
        """Helper Function = get widget index that we click into/drop into"""
        for i in range(self.count()):
            print(i)
            contains = self.itemAt(i).geometry().contains(pos)
            if contains and i != self.target:
                return i

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.eventTrap is None:
                self.eventTrap = event
                self.target = self.get_index(event.scenePosition().toPoint())
                print('-->', event.scenePosition().toPoint(), self.target)
            elif self.eventTrap == event:
                pass
            else:
                print("Something broke")
        else:
            self.target = None

    def mouseReleaseEvent(self, event):
        """
        This event just reinitialise the target and trap
        """
        self.target = None
        self.eventTrap = None

    def mouseMoveEvent(self, event:QtGui.QMouseEvent):
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.target is not None:
            print(self.target)
            drag = QtGui.QDrag(self.itemAt(self.target).widget())
            pix = self.itemAt(self.target).widget().grab()
            #print(self.itemAt(self.target).objectName())
            mimedata = QtCore.QMimeData()
            print(mimedata.imageData())
            mimedata.setImageData(pix)
            drag.setMimeData(mimedata)
            drag.setPixmap(pix)
            drag.setHotSpot(event.pos())
            a = drag.exec()
            print(a)
        else:
            pass



    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event:QtGui.QDropEvent):
        """Check if swap needs to occur and perform swap if so. """
        eventSource:QVBoxLayout = event.source() # For typehinting the next line
        if not eventSource.geometry().contains(event.position().toPoint()):
            source = self.get_index(event.position().toPoint())
            if source is None:
                self.eventTrap = None
                self.target = None
                return

            i, j = max(self.target, source), min(self.target, source)
            p1, p2 = self.grid.getItemPosition(i), self.grid.getItemPosition(j)

            # Update widget.lbl prior to moving items, while item handles are useful
            #self.grid.itemAt(i).widget().relabel(p2[0],p2[1])
            #self.grid.itemAt(j).widget().relabel(p1[0],p1[1])

            # The magic - pop item out of grid, then add item at new row/col/rowspan/colspan
            self.grid.addItem(self.grid.takeAt(i), *p2)
            self.grid.addItem(self.grid.takeAt(j), *p1)
            # Always reset our event trap & target handles.
            self.target = None
            self.eventTrap = None
        '''

class LabelImage(QLabel):
    '''
    This class modifies sligtly the QPlainTextEdit
    '''
    def __init__(self, content):
        '''
        A generic QPlainTextEdit widget

        Parameters
        ----------
        startup     :   list
                        list of things to display at startup
        font        :   str
                        'medium' or 'small'
        readonly    :   Bool
                        Optional. If True (default),
                        this box can not be edited by user
        Return
        ------
        None
        '''
        super().__init__()

        ###add content
        self.setText(content)
        
        color = ['red', 'yellow', 'green']
        self.setStyleSheet("margin-left:10; margin-right:10; margin-top:10; margin-bottom:10; background-color : %s; color : black"%random.choice(color))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        ###accepting drops
        self.acceptDrops()

    def dragEnterEvent(self, event):
        data_type = "text/plain"
        if event.mimeData().hasFormat(data_type):
            event.accept()
        else:
            event.ignore()



###below is temporary
class PT(QPlainTextEdit):
    '''
    This class modifies sligtly the QPlainTextEdit
    '''
    def __init__(self, readonly=True):
        '''
        A generic QPlainTextEdit widget

        Parameters
        ----------
        startup     :   list
                        list of things to display at startup
        font        :   str
                        'medium' or 'small'
        readonly    :   Bool
                        Optional. If True (default),
                        this box can not be edited by user
        Return
        ------
        None
        '''
        super().__init__()
        self.acceptDrops()
    
    def dragEnterEvent(self, event):
        data_type = "text/plain"
        if event.mimeData().hasFormat(data_type):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        data_type = "text/plain"
        if event.mimeData().hasFormat(data_type):
            for i in event.mimeData().text().split('|'):
                self.appendPlainText(i+'\n')


