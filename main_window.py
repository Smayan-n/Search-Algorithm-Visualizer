#created using PyQt5
#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from startUpUI import StartUpUI
from solveMazeUI import SolveMazeUI
from createMazeUI import CreateMazeUI

#How the multiple UIs work:

    #The MainWindow class is the parent of the QMainWindow class (it is where all the UI's are displayed)
        #all the widgets are children of the MainWindow class
    
        #the StartUpUI and mazeUI classes inherit from QWidget and can have their own UI

        #each of these widget classes have their own UI which can be displayed on the mainWindow

#main parent UI window
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle("Maze Solver")
        
        self.startStartUpUI()

    def startStartUpUI(self):
        self.startWin = StartUpUI(self)
        self.setCentralWidget(self.startWin)
        self.startWin.loadBtn.clicked.connect(lambda: self.startMazeUI())
        self.startWin.createBtn.clicked.connect(lambda: self.startWin.create())
        self.show()

    def startMazeUI(self, maze_template = None):
        #option param to determine if user wants to load or create a maze
        self.mazeWin = SolveMazeUI(self, maze_template)
        self.setCentralWidget(self.mazeWin)
        self.show()

    def startCreateUI(self, dimentions = None):
        self.createWin = CreateMazeUI(self, dimentions)
        self.setCentralWidget(self.createWin)
        self.show()

def start():

    #driver code to create a new QMainWindow object
    app = QApplication(sys.argv)

    #creating the window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
   start()