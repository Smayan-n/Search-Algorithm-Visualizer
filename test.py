import sys

from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class App(QMainWindow):
    def __init__(self):
        super().__init__()


 
        self.toggle1()

    def toggle1(self):
        aa = a(self)
        self.setCentralWidget(aa)
        aa.x.clicked.connect(self.toggle2)
        self.show()
    
    def toggle2(self):
        bb = b(self)
        self.setCentralWidget(bb)
        bb.y.clicked.connect(self.toggle3)   
        self.show()
    
    def toggle3(self):
        cc = c(self)
        self.setCentralWidget(cc)
        cc.z.clicked.connect(self.toggle1)
        self.show()
        
class a(QWidget):
    def __init__(self, win):
        super(a, self).__init__(win)
        self.x = QPushButton('aaaaaaaaa', self)

class b(QWidget):
    def __init__(self, win):
        super(b, self).__init__(win)
        self.y = QPushButton('bbbbbb', self)

class c(QWidget):
    def __init__(self, win):
        super(c, self).__init__(win)
        self.z = QPushButton('ccccccc', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = App()
    gui.show()
    app.exec_()