from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from maze_text_to_array_converter import ConvertString
from constants import *

class CreateMazeUI(QWidget):
    def __init__(self, mainWin=None, dimentions = None):
        super(CreateMazeUI, self).__init__(mainWin)

        self.mainWin = mainWin

        #variable to store state of mouse left click
        self.leftMouseDown = False

        #fileDialog    
        self.fileDialog = QFileDialog() 

        #loop that calls update function every 10 ms
        loop = QTimer(self)
        loop.timeout.connect(self.updateLoop)
        loop.start(10)

        self.createMaze(dimentions)

    def createMaze(self, dimentions):

        self.rows, self.cols = dimentions
        self.initGame()
        self.initCreateUI()

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

                cell.setStyleSheet(STYLE1 + WHITE)#sets all cells to blank

            x = 0
            y += self.cell_size
    
    
    #UI for maze creation
    def initCreateUI(self):
        #cell type selection buttons
        type_widget = QWidget(self)
        type_widget.setFont(FONT1)
        type_widget.move(0, -10)
        type_layout = QBoxLayout(QBoxLayout.TopToBottom, type_widget)

        h_layout1 = QHBoxLayout()
        self.wall_btn = QRadioButton("Wall", type_widget)
        self.wall_btn.setChecked(True)
        wall_lbl = QLabel(type_widget)
        wall_lbl.setMinimumWidth(50)
        wall_lbl.setStyleSheet("background-color: " + GREY)
        h_layout1.addWidget(wall_lbl)
        h_layout1.addWidget(self.wall_btn)

        self.empty_btn = QRadioButton("Empty", type_widget)
        empty_lbl = QLabel(type_widget)
        empty_lbl.setMinimumWidth(50)
        empty_lbl.setStyleSheet("background-color: " + WHITE)
        h_layout1.addWidget(empty_lbl)
        h_layout1.addWidget(self.empty_btn)

        h_layout2 = QHBoxLayout()
        self.start_btn = QRadioButton("Start", type_widget)
        start_lbl = QLabel(type_widget)
        start_lbl.setMaximumWidth(50)
        start_lbl.setStyleSheet("background-color: " + BLUE)
        h_layout2.addWidget(start_lbl)
        h_layout2.addWidget(self.start_btn)

        h_layout3 = QHBoxLayout()
        self.goal_btn = QRadioButton("Goal", type_widget)
        goal_lbl = QLabel(type_widget)
        goal_lbl.setMaximumWidth(50)
        goal_lbl.setStyleSheet("background-color: " + RED)
        h_layout3.addWidget(goal_lbl)
        h_layout3.addWidget(self.goal_btn)

        type_layout.addLayout(h_layout1)
        type_layout.addLayout(h_layout2)
        type_layout.addLayout(h_layout3)

        #save and solve button
        btn_widget = QWidget(self)
        btn_widget.setFont(FONT1)
        btn_widget.move(500, -10)
        btn_layout = QVBoxLayout(btn_widget)

        save_btn = QPushButton("Save", btn_widget)
        save_btn.clicked.connect(self.saveMaze)
        save_btn.setMinimumSize(100, 50)

        self.solve_btn = QPushButton("Solve", btn_widget)
        self.solve_btn.clicked.connect(self.solveMaze)
        save_btn.setMinimumSize(100, 50)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(self.solve_btn)

    def parseUIMaze(self):
        #parsing the maze from the UI into a string
        string_maze_template = ""
        for r in self.cells:
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

    def solveMaze(self):

        string_maze_template = self.parseUIMaze()
        #converts string maze to 2D array
        maze_template = ConvertString(string_maze_template)
        #calling start method in MainWindow
        self.mainWin.startMazeUI(maze_template)

    def saveMaze(self):
        
        self.maze_template = self.parseUIMaze()

        filePath = self.fileDialog.getSaveFileName(self, "Save Maze", "", "Text files (*.txt)")[0]
        
        with open(filePath, "w") as f:
            f.write(self.maze_template)


    #called when mouse is clicked
    def updateCell(self):
        #gets widget that that cursor is currently hovering over

        widget = qApp.widgetAt(QCursor.pos())
        #widget has to be a QLabel and has to be only a maze cell (not any other label). option also has to be "create"
        if type(widget) == QLabel and (widget.width(), widget.height()) == (self.cell_size, self.cell_size):
            
            if self.start_btn.isChecked():
                color = BLUE
            elif self.goal_btn.isChecked():
                color = RED
            elif self.empty_btn.isChecked():
                color = WHITE
            else:
                color = GREY
            
            widget.setStyleSheet(STYLE1 + color)

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
