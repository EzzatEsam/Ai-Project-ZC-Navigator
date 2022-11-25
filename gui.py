## We will not use this

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication , QMainWindow ,QWidget , QLabel
import sys


class gui_window :
    def __init__(self) -> None:
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle('Zc path')
        
        window.setGeometry(0,0,1000,700)
        window.show()
        label1 = QLabel(window)
        map_picture = QPixmap('map.png')
        label1.setPixmap(map_picture)
        window.setCentralWidget(label1)
        self.window = window
        sys.exit(app.exec_())

