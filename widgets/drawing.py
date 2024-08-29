from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np
import cv2

def show_mask(filename, mask, color):
    pixmap = QPixmap(filename)
    newPixamp = QPixmap(pixmap.size())
    
    h, w = mask.shape
    maskImage = np.array(mask.reshape(h, w, 1) * color.reshape(1, 1, -1), dtype=np.uint8)
    QmaskImage = QImage(maskImage.data, w, h, w*4, QImage.Format_RGBA8888)
    
    painter = QPainter(newPixamp)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    
    painter = QPainter(newPixamp)
    painter.setOpacity(0.6)
    painter.drawImage(0, 0, QmaskImage)
    painter.end()
    
    return newPixamp

    