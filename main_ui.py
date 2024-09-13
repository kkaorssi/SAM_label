from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import qdarkstyle

import sys

from widgets.fileio import tools
from widgets.dockers import list_docker
from widgets.canvas import iamge_label
from widgets.action import *
from widgets.dialog import *

UI_PATH = 'interface/mainwindow.ui'

mainwindow = uic.loadUiType(UI_PATH)[0]
# if you changed resource, excute the command below
# pyrcc5 interface/tools.qrc -o tools_rc.py

class WindowClass(QMainWindow, mainwindow) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # load widgets
        self.fileio = tools(self)
        self.dockers = list_docker(self)
        self.canvas = iamge_label(self)
        self.manager = action_manager()
        
        # Disable actions
        self.actionNext_Image.setDisabled(True)
        self.actionPrev_Image.setDisabled(True)
        self.actionSet_Image.setDisabled(True)
        self.actionSave.setDisabled(True)
        self.actionSave_As.setDisabled(True)
        self.actionAdd_Object.setDisabled(True)
        self.actionAdd_Point.setDisabled(True)
        self.actionExclude_Point.setDisabled(True)
        self.actionReset_Object.setDisabled(True)
        self.actionDelete_Object.setDisabled(True)
        self.actionEdit_Object.setDisabled(True)
        self.actionEdit_Label.setDisabled(True)
        
        self.initUI()

    def initUI(self):
        self.edit_mode = None

        # File
        self.actionOpen.triggered.connect(self.fileio.open_image)
        self.actionOpen_Dir.triggered.connect(self.fileio.open_dir)
        self.actionNext_Image.triggered.connect(self.fileio.next_image)
        self.actionPrev_Image.triggered.connect(self.fileio.prev_image)
        self.actionQuit.triggered.connect(self.close)
        self.actionSave.triggered.connect(self.fileio.save)
        
        # Edit
        self.actionSet_Image.triggered.connect(self.canvas.set_image)
        self.actionAdd_Object.triggered.connect(self.add_object)
        self.actionAdd_Point.triggered.connect(self.add_point)
        self.actionExclude_Point.triggered.connect(self.exclude_point)
        # self.actionReset_Object.triggered.connect(self.reset_object)
        # self.actionDelete_Object.triggered.connect(self.delete_object)
        # self.actionEdit_Label.triggered.connect(self.edit_label)
        
        # Display Image
        self.scrollArea = QScrollArea(self.centralWidget())
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.canvas)
        self.setCentralWidget(self.scrollArea)
        
    def add_object(self):
        objName = getTextInputDialog(self)
        if objName is None:
            print('canceled')
        else:
            self.dockers.add_label(objName)
            self.dockers.add_obj(objName)
            self.canvas.create_obj(objName)
            self.edit_mode = 'add'
        
    def add_point(self):
        self.edit_mode = 'add'
        
    def exclude_point(self):
        self.edit_mode = 'exclude'

    # def reset_object(self):

    # def delete_object(self):
    #     self.edit_mode = None

    # def edit_label(self):

    def closeEvent(self, event):
        self.fileio.quit_app(event)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    myWindow = WindowClass() 
    myWindow.showMaximized()
    app.exec_()