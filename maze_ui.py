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
        
        self.setFixedSize(750, 750)
        self.setWindowTitle("Maze Solver")
        
        self.startStartUpUI()

    def startStartUpUI(self):
        self.startWin = StartUpUI(self)
        self.setCentralWidget(self.startWin)
        self.startWin.loadBtn.clicked.connect(lambda: self.startMazeUI("load"))
        self.startWin.createBtn.clicked.connect(lambda: self.startWin.create())
        self.show()

    def startMazeUI(self, option, dimentions = None):
        #option param to determine if user wants to load or create a maze
        self.mazeWin = MazeUI(self, option, dimentions)
        self.setCentralWidget(self.mazeWin)
        self.show()

#UI that is displayed at the start of the program
class StartUpUI(QWidget):
    def __init__(self, mainWin=None):
        super(StartUpUI, self).__init__(mainWin)

        self.mainWin = mainWin

        #fonts
        self.font1 = QFont("Arial", 15)
        self.font2 = QFont("Arial", 18)

        #entry boxes for maze dimensions
        self.entry_box1 = None
        self.entry_box2 = None
        self.firstClick = True

        self.initUI()

    def initUI(self):

        #main vertical layout of the start screen
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        #labels
        info_lbl = QLabel("Welcome to the Maze Solver!")
        info_lbl.setFont(self.font1)
        info_lbl.setAlignment(QtCore.Qt.AlignCenter)

        maze_lbl = QLabel("Choose an action")
        maze_lbl.setFont(self.font2)
        maze_lbl.setAlignment(QtCore.Qt.AlignCenter)

        #two buttons that let user choose to create a maze or load a maze
        self.loadBtn = QPushButton("Load Maze", self)
        self.loadBtn.setFont(self.font1)
        self.loadBtn.setFixedHeight(150)
        self.createBtn = QPushButton("Create Maze", self)
        self.createBtn.setFont(self.font1)
        self.createBtn.setFixedHeight(150)

        self.layout.addWidget(info_lbl)
        self.layout.addWidget(maze_lbl)
        self.layout.addWidget(self.loadBtn)
        self.layout.addWidget(self.createBtn)

    #displays a prompt to enter maze dimensions
    def create(self):
        #the initializing of the widgets ibly happens on the first click of the create maze button
        if self.firstClick:

            create_lbl = QLabel("Enter Maze Dimentions: ")
            create_lbl.setFont(self.font1)
            self.layout.addWidget(create_lbl)
            
            h_layout = QHBoxLayout()
            self.layout.addLayout(h_layout)

            self.entry_box1 = QLineEdit(self)
            self.entry_box1.setValidator(QIntValidator())
            self.entry_box1.setPlaceholderText("Rows")
            self.entry_box1.setFont(self.font1)
            self.entry_box1.setMinimumSize(200, 100)
            h_layout.addWidget(self.entry_box1)

            x_lbl = QLabel("X")
            x_lbl.setFont(self.font1)
            h_layout.addWidget(x_lbl)        

            self.entry_box2 = QLineEdit(self)
            self.entry_box2.setValidator(QIntValidator())
            self.entry_box2.setPlaceholderText("Columns")
            self.entry_box2.setFont(self.font1)
            self.entry_box2.setMinimumSize(200, 100)
            h_layout.addWidget(self.entry_box2)

            self.firstClick = False
        
        else:

            #if the user has already entered the maze dimensions, then the program will start the maze UI
            if self.entry_box1.text() != "" and self.entry_box2.text() != "":
                rows = int(self.entry_box1.text())
                cols = int(self.entry_box2.text())
                #validating dimentions range
                if rows > 25: self.setError(self.entry_box1)
                else: self.clearError(self.entry_box1)
                if cols > 55: self.setError(self.entry_box2)
                else: self.clearError(self.entry_box2)

                if rows <= 25 and cols <= 55:
                    #passing option and dimensions to startMazeUI
                    self.mainWin.startMazeUI("create", (int(self.entry_box1.text()), int(self.entry_box2.text())))

            else:   
                if self.entry_box1.text() == "": self.setError(self.entry_box1)
                else: self.clearError(self.entry_box1)
                if self.entry_box2.text() == "": self.setError(self.entry_box2)
                else: self.clearError(self.entry_box2)
    

    #sets red border around entry box
    def setError(self, box):
        box.setStyleSheet("border: 3px solid red")
    def clearError(self, box):
        box.setStyleSheet("border: none")


#main maze UI
class MazeUI(QWidget):
    def __init__(self, mainWin=None, option=None, dimentions=None):
        super(MazeUI, self).__init__(mainWin)


        self.mainWin = mainWin
        self.option = option
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
        self.RED = "rgb(150, 0, 0)"
        self.BLUE = "rgb(0, 0, 150)"
        self.WHITE = "rgb(255, 255, 255)"
        self.YELLOW = "rgb(200, 200, 0)"
        
        #calling load/create function depending on option
        if self.option == "load":
            self.loadMaze()
        else:
            self.createMaze(dimentions)
    
    def createMaze(self, dimentions):

        self.rows, self.cols = dimentions
        self.initGame()
        self.initCreateUI()

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

        #widget is accesed by self keyword
        self.mainWin.setWindowTitle("Maze Solver")

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
                
                #alligns text in label to center
                cell.setAlignment(QtCore.Qt.AlignCenter)

                #determines placement and size of label
                cell.setGeometry(x, y, self.cell_size, self.cell_size)
                x += self.cell_size

                #calls loadMazeStyle only if "load" option was selected
                if self.option == "load":
                    self.loadMazeStyle(cell, row, col)  
                else:
                    cell.setStyleSheet("border: 1px solid rgb(0, 0, 0); background-color: white")   

            x = 0
            y += self.cell_size

    
    #sets style for label depending on contents of maze_template
    #color key:
    #white = empty cell, green = path, blue = end, grey = wall, red = goal
    def loadMazeStyle(self, cell, row, col):

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

    #UI for maze solving
    def initLoadUI(self):
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
        self.speed_label.setFont(self.font2)
        self.speed_label.setFixedSize(175, 50)

        self.speed_slider.valueChanged.connect(lambda: self.speed_label.setText("Speed: " + str(self.speed_slider.value()) + "   "))

        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)

        #button to solve maze
        solve_btn = QPushButton("Solve maze", self)
        solve_btn.setGeometry(800, 80, 200, 80)
        solve_btn.setStyleSheet("background-color: " + self.GREEN)
        solve_btn.clicked.connect(self.solveMaze)
        solve_btn.setFont(self.font2)

    #UI for maze creation
    def initCreateUI(self):
        #cell type selection buttons
        type_widget = QWidget(self)
        type_widget.setFont(self.font2)
        type_widget.move(0, -10)
        type_layout = QBoxLayout(QBoxLayout.TopToBottom, type_widget)

        h_layout1 = QHBoxLayout()
        self.wall_btn = QRadioButton("Wall", type_widget)
        self.wall_btn.setChecked(True)
        wall_lbl = QLabel(type_widget)
        wall_lbl.setMinimumWidth(50)
        wall_lbl.setStyleSheet("background-color: " + self.GREY)
        h_layout1.addWidget(wall_lbl)
        h_layout1.addWidget(self.wall_btn)

        self.empty_btn = QRadioButton("Empty", type_widget)
        empty_lbl = QLabel(type_widget)
        empty_lbl.setMinimumWidth(50)
        empty_lbl.setStyleSheet("background-color: " + self.WHITE)
        h_layout1.addWidget(empty_lbl)
        h_layout1.addWidget(self.empty_btn)

        h_layout2 = QHBoxLayout()
        self.start_btn = QRadioButton("Start", type_widget)
        start_lbl = QLabel(type_widget)
        start_lbl.setMaximumWidth(50)
        start_lbl.setStyleSheet("background-color: " + self.BLUE)
        h_layout2.addWidget(start_lbl)
        h_layout2.addWidget(self.start_btn)

        h_layout3 = QHBoxLayout()
        self.goal_btn = QRadioButton("Goal", type_widget)
        goal_lbl = QLabel(type_widget)
        goal_lbl.setMaximumWidth(50)
        goal_lbl.setStyleSheet("background-color: " + self.RED)
        h_layout3.addWidget(goal_lbl)
        h_layout3.addWidget(self.goal_btn)

        type_layout.addLayout(h_layout1)
        type_layout.addLayout(h_layout2)
        type_layout.addLayout(h_layout3)

        #save and solve button
        btn_widget = QWidget(self)
        btn_widget.setFont(self.font2)
        btn_widget.move(500, -10)
        btn_layout = QVBoxLayout(btn_widget)

        save_btn = QPushButton("Save", btn_widget)
        save_btn.clicked.connect(self.saveMaze)
        save_btn.setMinimumSize(100, 50)

        solve_btn = QPushButton("Solve", btn_widget)
        solve_btn.clicked.connect(self.saveMaze)
        save_btn.setMinimumSize(100, 50)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(solve_btn)

    def saveMaze(self):

        pass

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
        #widget has to be a QLabel and has to be only a maze cell (not any other label)
        if type(widget) == QLabel and (widget.width(), widget.height()) == (self.cell_size, self.cell_size):
            
            if self.start_btn.isChecked():
                color = self.BLUE
            elif self.goal_btn.isChecked():
                color = self.RED
            elif self.empty_btn.isChecked():
                color = self.WHITE
            else:
                color = self.GREY
            
            widget.setStyleSheet("border: 1px solid black; background-color: " + color)

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