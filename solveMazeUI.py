from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from maze_text_to_array_converter import convertTextFile
from maze_solver import MazeSolver
from constants import *

#main maze UI
class SolveMazeUI(QWidget):
    def __init__(self, mainWin=None, maze_template=None):
        super(SolveMazeUI, self).__init__(mainWin)

        self.mainWin = mainWin
        self.maze_template = maze_template

        #fileDialog    
        self.fileDialog = QFileDialog() 

        if self.maze_template is not None:
            #defines rows and cols in maze
            self.rows = len(self.maze_template)
            self.cols = max(len(row) for row in self.maze_template)
            self.initGame()
            self.initLoadUI()
        else:
            #calling load function 
            self.loadMaze()

    def loadMaze(self):

        #propmpts user to select a file
        filePath = self.fileDialog.getOpenFileName(self, "Open a maze", "", "Text Files (*.txt)")[0]
        #parses text file and stores in a 2D array
        self.maze_template = convertTextFile(filePath)

        #defines number of rows and columns in the maze
        self.rows = len(self.maze_template)
        #width is taken as longest row
        self.cols = max(len(row) for row in self.maze_template)

        #maze is initialized
        self.initGame()
        #widgets above maze initialized
        self.initLoadUI()


    #function to init variables 
    def initGame(self):

        #creating a 2D array of labels
        #each label acts like a cell/position in the maze
        self.cells = [[QLabel(self) for i in range(self.cols)] for j in range(self.rows)]
        
        #calls method to init UI
        self.initMaze()

    #initialization of maze grid
    def initMaze(self):

        #dimention of each square cell
        self.cell_size = 60

        #space for buttons and controls above the maze
        self.ctrl_spacing = 200

        #sets self.cell_size of window. The ability to be resized is restricted
        win_width = self.cols * self.cell_size
        win_height = self.rows * self.cell_size + self.ctrl_spacing

        #width has to have a minimum size
        win_width = max(win_width, 1200)

        self.mainWin.setFixedSize(win_width, win_height)

        #loops through cells and displays them
        x = 0
        y = self.ctrl_spacing
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                
                #alligns text in label to the center
                cell.setAlignment(QtCore.Qt.AlignCenter)

                #determines placement and size of label
                cell.setGeometry(x, y, self.cell_size, self.cell_size)
                x += self.cell_size

                self.loadMazeStyle(cell, row, col)  #sets style of cell

            x = 0
            y += self.cell_size
    
    #sets style for label depending on contents of maze_template
    #color key:
    #white = empty cell, green = path, blue = end, grey = wall, red = goal
    def loadMazeStyle(self, cell, row, col):

        color = WHITE
        try:
            cellState = self.maze_template[row][col]
            
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


    #UI for maze solving
    def initLoadUI(self):
        #widgets above the maze grid
        
        #solving method buttons
        radio_widget = QWidget(self)
        radio_widget.setFont(FONT1)
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
        check_box_widget.setFont(FONT1)
        check_box_widget.move(350, -10)
        check_box_layout = QHBoxLayout(check_box_widget)
        self.show_explored_checkBox = QCheckBox("Show explored states", check_box_widget)
        check_box_layout.addWidget(self.show_explored_checkBox)

        #speed slider
        speed_widget = QWidget(self)
        speed_widget.move(750, -10)
        speed_layout = QHBoxLayout(speed_widget)
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setFixedSize(200, 50)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(50)

        self.speed_label = QLabel("Speed: " + str(self.speed_slider.value()), self)
        self.speed_label.setFont(FONT1)
        self.speed_label.setFixedSize(175, 50)

        self.speed_slider.valueChanged.connect(lambda: self.speed_label.setText("Speed: " + str(self.speed_slider.value()) + "   "))

        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)

        #button to solve maze
        self.solve_btn = QPushButton("Solve maze", self)
        self.solve_btn.setGeometry(800, 80, 200, 80)
        self.solve_btn.setStyleSheet("background-color: " + GREEN)
        self.solve_btn.clicked.connect(self.solveMaze)
        self.solve_btn.setFont(FONT1)

    #solves maze
    def solveMaze(self):

        #resetting maze to it's unsolved state
        self.initMaze()
        #this block ensures that the user spamming the solvr button will not have any unintended consequences
        try:
            self.loop2.stop()
        except:
            pass

        maze_solver = MazeSolver()
        maze_solver.parse_maze(self.maze_template)

        #returns all the states in the path of the solution
        if self.a_star_btn.isChecked():
            method = "A* Search"
        elif self.bfs_btn.isChecked():
            method = "Breadth First Search"
        else:
            method = "Depth First Search"

        #Note: The explored states also contain the solution states
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
        self.loop2.timeout.connect(self.illustrateSolution)
        self.loop2.start(self.speed_slider.value())#using user specified speed

        self.index = 0

    #a looped function that is used to illustrate the maze being solved
    def illustrateSolution(self):

        explored_cell_x, explored_cell_y = self.display_solution[self.index]

        #finding the cell that corresponds to the explored state in display_solution
        cell = self.cells[explored_cell_x][explored_cell_y]
        #settin cell green if it is a solution state and yellow if it is just an explored state
        if (explored_cell_x, explored_cell_y) in self.solution:
            cell.setStyleSheet(STYLE1 + GREEN)
        else:
            cell.setStyleSheet(STYLE1 + YELLOW)

        self.index += 1
        if self.index == len(self.display_solution):
            self.index = 0
            self.loop2.stop()
