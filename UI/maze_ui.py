#created using PyQt5

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random, sys

class Window(QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        #variable to store state of mouse left click
        self.leftMouseDown = False

        #loop that calls update function every 10 ms
        loop = QTimer(self)
        loop.timeout.connect(self.updateLoop)
        loop.start(10)

        #fonts 
        self.font1 = QFont("Aerial", 12)
        self.font2 = QFont("Aerial", 8)

        #colors
        self.BG_COLOR = "rgb(100, 100, 100)"

        #defines number of rows and columns in the maze
        self.cols, self.rows = 20, 20
        self.initGame()

    #function to init variables 
    def initGame(self):

        #creating a 2D array of labels
        #each label acts like a cell/position in the maze
        self.cells = [[QLabel(self) for i in range(self.cols)] for j in range(self.rows)]

        #calls method to init UI
        self.initUI()


    #initialization of window and ui
    def initUI(self):

        #dimention of each square cell
        cellSize = 60

        #space for buttons and controls above the maze
        ctrl_spacing = 150

        #widget is accesed by self keyword
        self.setWindowTitle("Maze Solver")

        #sets cellSize of window. The ability to be resized is restricted
        win_width = self.cols * cellSize
        win_height = self.rows * cellSize +ctrl_spacing
        self.setGeometry(500, 100, win_width, win_height)

        #setting bg color of window
        self.setStyleSheet("background: " + self.BG_COLOR) 

        #loops through cells and displays them
        x = 0
        y = ctrl_spacing
        for list in self.cells:
            for label in list:
                
                #alligns text in label to center
                label.setAlignment(QtCore.Qt.AlignCenter)

                #determines placement and size of label
                label.setGeometry(x, y, cellSize, cellSize)
                x += cellSize

                #style of the label
                label.setStyleSheet("border: 1px solid rgb(0, 0, 0); background-color: white")          

            x = 0
            y += cellSize

        #widgets above the maze grid

        #checkbox to toggle between showing only solution and explored states as well
        self.checkBox = QCheckBox("Show explored states", self)
        self.checkBox.setFont(self.font1)
        self.checkBox.setGeometry(500, int(ctrl_spacing / 2 - self.checkBox.width()/2), 500, 100)

        self.comboBox = QComboBox(self)
        self.comboBox.setFont(self.font2)
        self.comboBox.setGeometry(10, int(ctrl_spacing/2), 300, 75)
        self.comboBox.setStyleSheet("background-color: white")
        self.comboBox.addItem("A* search")
        self.comboBox.addItem("Depth-First Search")
        self.comboBox.addItem("Breadth-First Search")


    #called when mouse is clicked
    def updateCell(self):
        #gets widget that thae cursor is currently hovering over
        widget = qApp.widgetAt(QCursor.pos())
        if type(widget) == QLabel:
            
            widget.setStyleSheet("border: 1px solid rgb(0, 0, 0); background-color: rgb(0, 255, 0)")

    def mousePressEvent(self, event):   
        if event.button() == Qt.LeftButton:
            self.updateCell()  
            self.leftMouseDown = True

    def mouseReleaseEvent(self, event):    
        if event.button() == Qt.LeftButton: 
            self.leftMouseDown = False

    #loop function that gets called by loop
    def updateLoop(self):
        if self.leftMouseDown:
            self.updateCell()
       

def start():

    #driver code to create a new QMainWindow object
    app = QApplication(sys.argv)

    #creating the window
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
   start()