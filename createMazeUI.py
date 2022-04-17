from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from numpy import save

from maze_text_to_array_converter import ConvertString
from constants import *

#class handles that UI that is used for the creation of mazes
#it can also be used to load mazes and edit them
class CreateMazeUI(QWidget):
    def __init__(self, mainWin=None, dimentions = None, maze_template = None):
        super(CreateMazeUI, self).__init__(mainWin)

        self.mainWin = mainWin
        self.maze_template = maze_template

        #variable to store state of mouse  click
        self.leftMouseDown = False
        self.rightMouseDown = False

        #fileDialog    
        self.fileDialog = QFileDialog() 

        #loop that calls update function every 10 ms
        loop = QTimer(self)
        loop.timeout.connect(self.updateLoop)
        loop.start(10)

        #maze template passed in so load maze
        if maze_template is not None:
            #defines rows and cols in maze
            self.rows = len(self.maze_template)
            self.cols = max(len(row) for row in self.maze_template)
            self.initGame(maze_template)
            self.initCreateUI()
        #if mo maze template is passed in, then create empty maze
        else:
            self.createMaze(dimentions)


    def createMaze(self, dimentions):

        self.rows, self.cols = dimentions
        self.initGame()
        self.initCreateUI()

    #function to init variables 
    def initGame(self, maze_template = None):

        #creating a 2D array of labels
        #each label acts like a cell/position in the maze
        self.cells = [[QLabel(self) for i in range(self.cols)] for j in range(self.rows)]

        #calls method to init UI
        self.mainWin.initMaze(self.cells, maze_template)

   
    def solveMaze(self):

        string_maze_template = self.mainWin.parseUIMaze(self.cells)
        #converts string maze to 2D array
        maze_template = ConvertString(string_maze_template)
        #calling start maze solve method in MainWindow (passing in template to load)
        self.mainWin.startMazeUI(maze_template)

    #called when mouse is clicked
    def updateCell(self):
        #gets widget that that cursor is currently hovering over

        widget = qApp.widgetAt(QCursor.pos())
        #widget has to be a QLabel and has to be only a maze cell (not any other label).
        if type(widget) == QLabel:
            #only maze cells have this size
            if widget.size() == QSize(MAZE_CELL_SIZE, MAZE_CELL_SIZE):
                
                if self.start_btn.isChecked():
                    color = BLUE
                elif self.goal_btn.isChecked():
                    color = RED
                elif self.empty_btn.isChecked():
                    color = WHITE
                else:
                    color = GREY
                
                widget.setStyleSheet(STYLE1 + color)
            
            #if not a maze cell, then it is the radio button labels
            #radio buttons are toggled based on the label clicked
            else:
                if widget.styleSheet() == STYLE1 + GREY:
                    self.wall_btn.setChecked(True)
                elif widget.styleSheet() == STYLE1 + RED:
                    self.goal_btn.setChecked(True)
                elif widget.styleSheet() == STYLE1 + BLUE:
                    self.start_btn.setChecked(True)
                else:
                    self.empty_btn.setChecked(True)

    def mousePressEvent(self, event):   
        if event.button() == Qt.LeftButton:
            self.leftMouseDown = True
        if event.button() == Qt.RightButton:
            self.rightMouseDown = True
        
        self.updateCell()

    def mouseReleaseEvent(self, event):    
        if event.button() == Qt.LeftButton: 
            self.leftMouseDown = False
        if event.button() == Qt.RightButton:
            self.rightMouseDown = False
        
    #loop function that gets called by loop
    def updateLoop(self):
        if self.leftMouseDown:
            self.updateCell()

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
        wall_lbl.setFixedSize(MAZE_CELL_SIZE -1, MAZE_CELL_SIZE-1)
        wall_lbl.setStyleSheet(STYLE1 + GREY)

        self.empty_btn = QRadioButton("Empty", type_widget)
        empty_lbl = QLabel(type_widget)
        empty_lbl.setFixedSize(MAZE_CELL_SIZE-1, MAZE_CELL_SIZE-1)
        empty_lbl.setStyleSheet(STYLE1 + WHITE)

        h_layout1.addWidget(wall_lbl)
        h_layout1.addWidget(self.wall_btn)
        h_layout1.addSpacing(25)
        h_layout1.addWidget(empty_lbl)
        h_layout1.addWidget(self.empty_btn)

        h_layout2 = QHBoxLayout()
        self.start_btn = QRadioButton("Start", type_widget)
        start_lbl = QLabel(type_widget)
        start_lbl.setFixedSize(MAZE_CELL_SIZE-1, MAZE_CELL_SIZE-1)
        start_lbl.setStyleSheet(STYLE1 + BLUE)
        h_layout2.addWidget(start_lbl)
        h_layout2.addWidget(self.start_btn)

        #clear button
        clear_btn = QPushButton("Clear", type_widget)
        clear_btn.clicked.connect(lambda: self.mainWin.resetMaze(self.cells))
        clear_btn.setStyleSheet("background-color: " + ORANGE + "; color: " + WHITE)
        h_layout2.addWidget(clear_btn)

        h_layout3 = QHBoxLayout()
        self.goal_btn = QRadioButton("Goal", type_widget)
        goal_lbl = QLabel(type_widget)
        goal_lbl.setFixedSize(MAZE_CELL_SIZE-1, MAZE_CELL_SIZE-1)
        goal_lbl.setStyleSheet(STYLE1 + RED)
        h_layout3.addWidget(goal_lbl)
        h_layout3.addWidget(self.goal_btn)

        type_layout.addLayout(h_layout1)
        type_layout.addSpacing(10)
        type_layout.addLayout(h_layout2)
        type_layout.addSpacing(10)
        type_layout.addLayout(h_layout3)

        #save and solve button
        btn_widget = QWidget(self)
        btn_widget.setFont(FONT1)
        btn_widget.move(550, -10)
        btn_layout = QVBoxLayout(btn_widget)

        solve_btn = QPushButton("Solve maze", btn_widget)
        solve_btn.setStyleSheet("background-color: " + GREEN)
        solve_btn.setFont(FONT1)
        solve_btn.clicked.connect(self.solveMaze)
        solve_btn.setMinimumHeight(100)

        save_btn = QPushButton("Save maze", btn_widget)
        save_btn.setStyleSheet("background-color: " + GREEN)
        save_btn.setFont(FONT1)
        save_btn.clicked.connect(lambda: self.mainWin.saveMaze(self.cells))
        save_btn.setMinimumHeight(75)

        btn_layout.addWidget(solve_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(save_btn)