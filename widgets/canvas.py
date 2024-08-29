import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from qimage2ndarray import *

import cv2
import numpy as np

from widgets.dialog import *
from widgets.drawing import *

class iamge_label(QLabel):
    def __init__(self, mainwindow):
        super().__init__()
        
        self.mainwindow = mainwindow
        self.mode = None
        
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setMouseTracking(True)
        self.setPixmap(QPixmap())
        
        self.mouseReleaseEvent = self.on_label_release
        
        self.color = np.concatenate([np.random.randint(low=0, high=256, size=3, dtype=np.uint8), 
                    np.array([255])], axis=0)
        
    # def mouseMoveEvent(self, event):
    #     x = event.pos().x()
    #     y = event.pos().y()
    #     input_point = np.array([[x, y]])
    #     input_label = np.array([1])
    #     if self.mode == 'Manual':
    #         mask, scores, logits = self.mainwindow.predict.add_point(self.predictor, input_point, input_label)
    #         newPixmap = show_mask(self.filename, mask, self.color)
    #         self.setPixmap(newPixmap)
    
    def on_label_release(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            input_point = [int(x), int(y)]
            count = self.mainwindow.dockers.objlist.count()
            if count == 0 or self.mainwindow.edit_mode is None:
                return
            w = self.qpixmap.width()
            h = self.qpixmap.height()
            if x > w or y > h:
                return
            current_obj = self.mainwindow.dockers.objlist.currentItem()
            if current_obj is None:
                return
            objIdx = self.mainwindow.dockers.objlist.currentRow()
            if self.mainwindow.edit_mode == 'add':
                mask = self.mainwindow.manager.add_point(self.filename, objIdx, input_point, self.mode)
            elif self.mainwindow.edit_mode == 'exclude':
                mask = self.mainwindow.manager.exclude_point(self.filename, objIdx, input_point, self.mode)
            newpixmap = show_mask(self.filename, mask, self.color)
            self.setPixmap(newpixmap)
            
    def display_image(self, filename):
        self.filename = filename
        self.qpixmap = QPixmap(filename)
        self.setPixmap(self.qpixmap)
        self.mode = None
        
    def set_image(self):
        temp, reply = choose_mode(self.mainwindow)
        if not reply:
            print('mode is not selected')
        else:
            self.mode = temp
            pixmap = self.qpixmap
            qimage = pixmap.toImage()
            image = rgb_view(qimage)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.mainwindow.manager.regist_file(self.filename, image, self.mode)
            self.mainwindow.actionAdd_Object.setEnabled(True)
            
            obj_list = self.mainwindow.manager.get_data(self.filename, self.mode)
            if not obj_list is None:
                self.mainwindow.dockers.objlist.addItems(obj_list)
                
    def create_obj(self, objName):
        self.mainwindow.manager.create_obj(self.filename, objName, self.mode)

    # def reset_obj(self, objIdx):

    # def delete_obj(self, objIdx):

    # def rename_label(self, objIdx, newName):