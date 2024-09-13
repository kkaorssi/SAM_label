from PyQt5.QtWidgets import *

import os
import pandas as pd
import json
import cv2
import numpy as np

class tools:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

    def open_image(self):
        filename = QFileDialog.getOpenFileName(self.mainwindow, caption='Open Image', filter='Image(*.jpg *.jpeg *.png)')
        if filename[0]:
            self.mainwindow.dockers.filelist.clear()
            item = QListWidgetItem(filename[0], self.mainwindow.dockers.filelist)
            self.mainwindow.dockers.filelist.setCurrentItem(item)
            
        else:
            print("File not selected")

    def open_dir(self):
        dirname = QFileDialog.getExistingDirectory(self.mainwindow, caption='Open Directory')
        if dirname:
            print('folder: ', dirname)

            fnames = os.listdir(dirname)
            f_list = []
            for fname in fnames:
                f_name, f_ext = os.path.splitext(fname)
                if f_ext == '.jpg' or '.JPEG' or '.png':
                    filename = os.path.join(dirname, fname)
                    f_list.append(filename)

            self.mainwindow.dockers.filelist.clear()
            self.mainwindow.dockers.filelist.addItems(f_list)
            self.mainwindow.dockers.filelist.setCurrentRow(0)

        else:
            print("Directory not selected")

    def next_image(self):
        currentRow = self.mainwindow.dockers.filelist.currentRow()
        nextItem = self.mainwindow.dockers.filelist.item(currentRow + 1)
        
        if nextItem is not None:
            # do something with the next item
            self.mainwindow.dockers.filelist.setCurrentRow(currentRow + 1)

        else:
            print("No next image")

    def prev_image(self):
        currentRow = self.mainwindow.dockers.filelist.currentRow()
        prevItem = self.mainwindow.dockers.filelist.item(currentRow - 1)
        
        if prevItem is not None:
            # do something with the next item
            self.mainwindow.dockers.filelist.setCurrentRow(currentRow - 1)

        else:
            print("No prev image")

    def save(self):
        json_data = {
            "version": "5.1.1",
            "flags": {},
            "shapes": [],
            "imagePath": os.path.basename(self.mainwindow.canvas.filename),
            "imageData": None,
            "imageHeight": self.mainwindow.canvas.qpixmap.height(),
            "imageWidth": self.mainwindow.canvas.qpixmap.width()
        }
        
        for i in range(self.mainwindow.dockers.objlist.count()):
            item = self.mainwindow.dockers.objlist.item(i)
            label = item.text()
            
            mask = np.array(self.mainwindow.canvas.mask, dtype=np.uint8)
            edges = cv2.Canny(mask * 255, 100, 200) 
            points = np.argwhere(edges > 0)
            points_list = points.tolist() 

            shape_data = {
                "label": label,
                "points": points_list,
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
            json_data["shapes"].append(shape_data)
        
        f_name, f_ext = os.path.splitext(self.mainwindow.canvas.filename)
        save_path = f"{f_name}.json"
        with open(save_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
            print(f"JSON file saved to {save_path}")
            
    # def save_as(self):

    # def save_auto(self):

    def quit_app(self, event):
        if self.mainwindow.dockers.unsaved == True:
            quit_msg = "Are you sure to quit?"
            reply = QMessageBox.question(self.mainwindow, 'Message', quit_msg, 
                                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Save:
                self.save()
                event.accept()
            elif reply == QMessageBox.Discard:
                print('file not saved')
                event.accept()
            else:
                print('Quit canceled')
                event.ignore()
