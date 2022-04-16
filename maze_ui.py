#created using PyQt5

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, time

from maze_text_parser import parseTextFile
from maze_solver import MazeSolver

#main parent UI window
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        self.setGeometry(400, 200, 500, 500)
        self.setFixedSize(500, 500)
        self.startStartUI()

    def startStartUI(self):
        self.startWin = StartUI(self)
        self.setCentralWidget(self.startWin)
        self.startWin.loadBtn.clicked.connect(lambda: self.startMazeUI("load"))
        self.startWin.createBtn.clicked.connect(lambda: self.startMazeUI("create"))
        self.show()

    def startMazeUI(self, option):
        #option param to determine if user wants to load or create a maze
        self.mazeWin = MazeUI(self, option)
        self.setCentralWidget(self.mazeWin)
        self.show()

#UI that is displayed at the start of the program
class StartUI(QWidget):
    def __init__(self, mainWin=None):
        super(StartUI, self).__init__(mainWin)

        #two buttons that let user choose to create a maze or load a maze
        self.loadBtn = QPushButton("Load maze", self)
        self.loadBtn.move(100, 100)
        self.createBtn = QPushButton("Create maze", self)
        self.createBtn.move(100, 200)

#main maze UI
class MazeUI(QWidget):
    def __init__(self, mainWin=None, option=None):
        super(MazeUI, self).__init__(mainWin)

        self.mainWin = mainWin

        #variable to store state of mouse left click
        self.leftMouseDown = False

        #loop that calls update function every 10 ms
        loop = QTimer(self)
        loop.timeout.connect(self.updateLoop)
        loop.start(10)

        #fonts 
        self.font1 = QFont("Aerial", 12)
        self.font2 = QFont("Aerial", 10)

        #colors
        self.BG_COLOR = "rgb(100, 100, 100)"
        self.GREEN = "rgb(0, 200, 0)"
        self.GREY = "rgb(100, 100, 100)"
        self.RED = "rgb(200, 0, 0)"
        self.BLUE = "rgb(0, 0, 200)"
        self.WHITE = "rgb(255, 255, 255)"
        self.YELLOW = "rgb(255, 255, 0)"
        
        self.rows = 10
        self.cols = 10

        if option == "load":
            self.loadMaze()
        else :
            self.createMaze()
    
    def createMaze(self):

        pass

    def loadMaze(self):

        #prompts user to select a file
        fileDialog = QFileDialog() 
        filePath = fileDialog.getOpenFileName()[0]

        #parses text file and stores in a 2D array
        self.maze_template = parseTextFile(filePath)
        #defines number of rows and columns in the maze
        self.rows = len(self.maze_template)
        #width is taken as longest row
        self.cols = max(len(row) for row in self.maze_template)

        #maze is initialized
        self.initGame()


    #function to init variables 
    def initGame(self):

        #creating a 2D array of labels
        #each label acts like a cell/position in the maze
        self.cells = [[QLabel(self) for i in range(self.cols)] for j in range(self.rows)]
        print(len(self.maze_template), len(self.maze_template[0]), len(self.cells), len(self.cells[0]))
        #calls method to init UI
        self.initMaze()
        self.initUI()

    #initialization of maze grid
    def initMaze(self):

        #dimention of each square cell
        cellSize = 60

        #space for buttons and controls above the maze
        ctrl_spacing = 200

        #widget is accesed by self keyword
        self.mainWin.setWindowTitle("Maze Solver")

        #sets cellSize of window. The ability to be resized is restricted
        win_width = self.cols * cellSize
        win_height = self.rows * cellSize + ctrl_spacing
        self.mainWin.setFixedSize(win_width, win_height)

        #loops through cells and displays them
        x = 0
        y = ctrl_spacing
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                
                #alligns text in label to center
                cell.setAlignment(QtCore.Qt.AlignCenter)

                #determines placement and size of label
                cell.setGeometry(x, y, cellSize, cellSize)
                x += cellSize

                #sets style for label depending on contents of maze_template
                #color key:
                #white = empty cell, green = path, blue = end, grey = wall, red = goal
                color = self.WHITE
                try:
                    cellState = self.maze_template[row][col]
                    
                    if cellState == 'A':
                        color = self.BLUE
                        
                    elif cellState == 'B':
                        color = self.RED
                    
                    if cellState == ' ':
                        color = self.WHITE
                        
                    elif cellState == '#':
                        #wall exists
                        color = self.GREY
                    
                except IndexError:
                    #for rows that are shorter that the rest, they are assumed to be clear cells
                    color = self.WHITE

                cell.setStyleSheet("border: 1px solid rgb(0, 0, 0); background-color: " + color)          

            x = 0
            y += cellSize

    #initializes the UI above the maze grid
    def initUI(self):
        #widgets above the maze grid
        
        #solving method buttons
        radio_widget = QWidget(self)
        radio_widget.setFont(self.font2)
        radio_widget.move(0, -10)
        radio_layout = QVBoxLayout(radio_widget)

        self.a_star_btn = QRadioButton("A* Search", radio_widget)
        self.a_star_btn.setChecked(True)
        self.bfs_btn = QRadioButton("Breadth First Fearch", radio_widget)
        self.dfs_btn = QRadioButton("Depth First Fearch", radio_widget)

        radio_layout.addWidget(self.a_star_btn)
        radio_layout.addWidget(self.bfs_btn)
        radio_layout.addWidget(self.dfs_btn)
       
        #checkbox to toggle between showing only solution and explored states as well
        check_box_widget = QWidget(self)
        check_box_widget.setFont(self.font2)
        check_box_widget.move(400, -10)
        check_box_layout = QHBoxLayout(check_box_widget)
        self.show_explored_checkBox = QCheckBox("Show explored states", check_box_widget)
        check_box_layout.addWidget(self.show_explored_checkBox)

        #speed slider
        speed_widget = QWidget(self)
        speed_widget.move(900, 10)
        speed_layout = QHBoxLayout(speed_widget)
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(500)
        self.speed_slider.setFixedSize(200, 50)

        self.speed_label = QLabel("Speed: " + str(self.speed_slider.value()), self)
        self.speed_label.setFont(self.font2)

        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)

        #button to solve maze
        solve_btn = QPushButton("Solve maze", self)
        solve_btn.clicked.connect(self.solveMaze)
        solve_btn.setFont(self.font2)
        solve_btn.move(900, 100)

    #solves maze
    def solveMaze(self):

        self.initMaze()

        maze_solver = MazeSolver()
        maze_solver.parse_maze(self.maze_template)

        #returns all the states in the path of the solution
        if self.a_star_btn.isChecked():
            method = "A* Search"
        elif self.bfs_btn.isChecked():
            method = "Breadth First Search"
        else:
            method = "Depth First Search"

        #NOTE: The explored states also contain the solution states
        self.solution, self.explored = maze_solver.solve_maze(method)

        #removing last state from solution since it is the goal state
        self.solution.pop()
        #removing first state from explored since it is the start state
        self.explored.pop(0)

        #display_solution will contain all the states that need to be displayed(explored and/or solution states)
        if self.show_explored_checkBox.isChecked():
            self.display_solution = self.explored
        else:
            self.display_solution = self.solution   

        #creating a loop/timer so the illustrate function can be called at regular intervals
        self.loop2 = QTimer(self)
        self.loop2.timeout.connect(self.illustrateSolve)
        #using user specified speed
        self.loop2.start(self.speed_slider.value())

        self.index = 0

    #a looped function that is used to illustrate the maze being solved
    def illustrateSolve(self):

        explored_cell_x, explored_cell_y = self.display_solution[self.index]

        #finding the cell that corresponds to the explored state in display_solution
        cell = self.cells[explored_cell_x][explored_cell_y]
        #settin cell green if it is a solution state and yellow if it is just an explored state
        if (explored_cell_x, explored_cell_y) in self.solution:
            cell.setStyleSheet("border: 1px solid rgb(0, 0, 0); background-color: " + self.GREEN)
        else:
            cell.setStyleSheet("border: 1px solid rgb(0, 0, 0); background-color: " + self.YELLOW)

        self.index += 1
        if self.index == len(self.display_solution):
            self.index = 0
            self.loop2.stop()


    #called when mouse is clicked
    def updateCell(self):
        #gets widget that that cursor is currently hovering over
        widget = qApp.widgetAt(QCursor.pos())
        if type(widget) == QLabel:
            
            widget.setStyleSheet("border: 1px solid black; background-color: " + self.GREEN)

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
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
   start()