#created using PyQt5
#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from maze_basic import Maze

from startUpUI import StartUpUI
from solveMazeUI import SolveMazeUI
from createMazeUI import CreateMazeUI
from constants import *

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

        self.fileDialog = QFileDialog()
        
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

    def startCreateUI(self, dimentions = None, maze_template = None):
        self.createWin = CreateMazeUI(self, dimentions, maze_template)
        self.setCentralWidget(self.createWin)
        self.show()

    #-------------------------------other helper methods------------------------------------------------#

    #resets maze to its original state
    def resetMaze(self, cells, maze_template=None):

        for row in range(len(cells)):
            for col in range(len(cells[row])):
                if maze_template is not None:
                    self.loadMazeStyle(cells[row][col], row, col, maze_template)
                else:
                    cells[row][col].setStyleSheet(STYLE1 + WHITE)

    #initialization of maze grid
    def initMaze(self, cells, maze_template=None):
        rows = len(cells)
        cols = len(cells[0])

        #sets MAZE_CELL_SIZE of window. The ability to be resized is restricted
        win_width = cols * MAZE_CELL_SIZE
        win_height = rows * MAZE_CELL_SIZE + MAZE_CTRL_SPACING

        #width has to have a minimum size
        win_width = max(win_width, MIN_WIN_WIDTH)

        self.setFixedSize(win_width, win_height)

        #loops through cells and displays them
        x = 0
        y = MAZE_CTRL_SPACING

        for row in range(rows):
            for col in range(cols):
                cell = cells[row][col]
                
                #alligns text in label to the center
                cell.setAlignment(QtCore.Qt.AlignCenter)

                #determines placement and size of label
                cell.setGeometry(x, y, MAZE_CELL_SIZE, MAZE_CELL_SIZE)
                x += MAZE_CELL_SIZE

                #sets style of label depending on option
                if maze_template is not None:
                    self.loadMazeStyle(cell, row, col, maze_template)  #sets style of cell
                else:
                    cell.setStyleSheet(STYLE1 + WHITE)

            x = 0
            y += MAZE_CELL_SIZE
    
    #sets style for label depending on contents of maze_template
    #color key:
    #white = empty cell, green = path, blue = end, grey = wall, red = goal
    def loadMazeStyle(self, cell, row, col, maze_template):

        color = WHITE
        try:
            cellState = maze_template[row][col]
            
            if cellState == 'A':
                color = BLUE
                
            elif cellState == 'B':
                color = RED
            
            if cellState == ' ':
                color = WHITE
                
            elif cellState == '#':
                #wall exists
                color = GREY
            
        except IndexError:
            #for rows that are shorter that the rest, they are assumed to be clear cells
            color = WHITE

        cell.setStyleSheet(STYLE1 + color)

    #spropmpts user to save maze as text file
    def saveMaze(self, maze_cells):
                
        self.maze_template = self.parseUIMaze(maze_cells)

        filePath = self.fileDialog.getSaveFileName(self, "Save Maze", "", "Text files (*.txt)")[0]
        
        with open(filePath, "w") as f:
            f.write(self.maze_template)
    
    #method that takes the maze UI grid and converts it to a string representation that can be saved in a text file
    def parseUIMaze(self, maze_cells):
        #parsing the maze from the UI into a string
        string_maze_template = ""
        for r in maze_cells:
            row = ""
            for cell in r:
                if cell.styleSheet() == STYLE1 + GREY:
                    row += "#"
                elif cell.styleSheet() == STYLE1 + BLUE:
                    row += "A"
                elif cell.styleSheet() == STYLE1 + RED:
                    row += "B"
                else:
                    row += " "
            
            string_maze_template += row + "\n"

        return string_maze_template

def start():

    #driver code to create a new QMainWindow object
    app = QApplication(sys.argv)

    #creating the window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
   start()