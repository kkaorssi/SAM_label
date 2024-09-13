from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class list_docker:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.initUI()

    def initUI(self):
        # label list
        self.labelDcok = QDockWidget('label list', self.mainwindow)
        self.labellist = QListWidget()
        self.labelDcok.setWidget(self.labellist)
        self.labelDcok.setFloating(False)
        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.labelDcok)

        # object list
        self.objDcok = QDockWidget('object list', self.mainwindow)
        self.objlist = QListWidget()
        self.objDcok.setWidget(self.objlist)
        self.objDcok.setFloating(False)
        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.objDcok)
        self.objlist.currentItemChanged.connect(self.object_changed)

        # file list
        self.fileDcok = QDockWidget('file list', self.mainwindow)
        self.filelist = QListWidget()
        self.fileDcok.setWidget(self.filelist)
        self.fileDcok.setFloating(False)
        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.fileDcok)
        self.filelist.currentItemChanged.connect(self.image_changed)
        self.unsaved = False
        
    def add_label(self, label):
        # check if label exists in the list widget
        matching_labels = self.labellist.findItems(label, Qt.MatchExactly)

        if not matching_labels:
            item = QListWidgetItem(label, self.mainwindow.dockers.labellist)
            self.mainwindow.dockers.labellist.setCurrentItem(item)
            
    def add_obj(self, label):
        item = QListWidgetItem(label, self.mainwindow.dockers.objlist)
        self.mainwindow.dockers.objlist.setCurrentItem(item)
        self.mainwindow.actionSave.setEnabled(True)
        self.mainwindow.actionSave_As.setEnabled(True)
    
    def object_changed(self, current, previous):
        if self.objlist.currentItem():
            self.mainwindow.actionAdd_Point.setEnabled(True)
            self.mainwindow.actionExclude_Point.setEnabled(True)
            self.mainwindow.actionReset_Object.setEnabled(True)
            self.mainwindow.actionDelete_Object.setEnabled(True)
            self.mainwindow.actionEdit_Object.setEnabled(True)
            self.mainwindow.actionEdit_Label.setEnabled(True)

    def image_changed(self, current, previous):
        self.mainwindow.actionSet_Image.setEnabled(True)
        if self.unsaved:
            msg = 'There are unsaved changes. Do you want to save them?'
            reply = QMessageBox.question(self.mainwindow, 'Message', msg, 
                                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.mainwindow.fileio.save()
            elif reply == QMessageBox.Discard:
                print('file not saved')
            else:
                self.filelist.blockSignals(True)
                self.filelist.setCurrentItem(previous)
                self.filelist.blockSignals(False)
                print('file selection canceled')
                return
            self.unsaved = False
            
        if self.filelist.currentItem():
            # reset options
            print('image: ', current.text())
            self.mainwindow.canvas.display_image(current.text())
            self.mainwindow.actionAdd_Object.setDisabled(True)
            self.mainwindow.actionAdd_Point.setDisabled(True)
            self.mainwindow.actionExclude_Point.setDisabled(True)
            self.mainwindow.actionReset_Object.setDisabled(True)
            self.mainwindow.actionDelete_Object.setDisabled(True)
            self.mainwindow.actionEdit_Object.setDisabled(True)
            self.mainwindow.actionEdit_Label.setDisabled(True)
            count = self.filelist.count()
            currentRow = self.filelist.currentRow()
            self.objlist.clear()
            
            if currentRow == 0:
                self.mainwindow.actionPrev_Image.setDisabled(True)
            else:
                self.mainwindow.actionPrev_Image.setEnabled(True)
                
            if currentRow+1 == count:
                self.mainwindow.actionNext_Image.setDisabled(True)
            else:
                self.mainwindow.actionNext_Image.setEnabled(True)
