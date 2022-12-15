## We will not use this

import typing
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication , QMainWindow ,QWidget , QLabel
from PyQt5 import QtCore
import sys


BLACK = (0,0,0) 
WHITE = (255,255,255) 
BLUE = (0, 0, 128)

MAP_POS = (0,0)
LABEL1_POS = (800,80)
LABEL2_POS = (800,160)
LABEL3_POS = (800,240)
WIDTH_HEIGHT = ( 1280 , 720)

class gui_handler :
    def __init__(self , gen) -> None:
        self.gen = gen
        app = QApplication(sys.argv)
        window = main_window(self)
        
        self.window = window
        sys.exit(app.exec_())

    def OnMousePressed(self,mouse_mos) :
        pass
        


class main_window(QMainWindow) :
    def __init__(self, handler ) -> None:
        super().__init__()
        self.handler = handler
        self.setWindowTitle('Zc path')
        self.setGeometry(0,0,WIDTH_HEIGHT[0],WIDTH_HEIGHT[1])
        self.show()
        map1 = QLabel(self)
        map_picture = QPixmap('map.png')
        map1.setPixmap(map_picture)
        self.setCentralWidget(map1)
    
    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())
        self.handler.OnMousePressed(QMouseEvent.pos())

