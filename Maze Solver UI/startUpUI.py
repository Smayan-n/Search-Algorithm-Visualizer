
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from constants import *

#UI that is displayed at the start of the program
class StartUpUI(QWidget):
    def __init__(self, mainWin=None):
        super(StartUpUI, self).__init__(mainWin)

        self.mainWin = mainWin
        self.mainWin.setFixedSize(750, 750)

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
        info_lbl.setFont(FONT3)
        info_lbl.setAlignment(QtCore.Qt.AlignCenter)

        maze_lbl = QLabel("Choose an action")
        maze_lbl.setFont(FONT3)
        maze_lbl.setAlignment(QtCore.Qt.AlignCenter)

        #two buttons that let user choose to createMaze a maze or load a maze
        self.loadBtn = QPushButton("Load Maze", self)
        self.loadBtn.setFont(FONT3)
        self.loadBtn.setFixedHeight(150)
        self.createBtn = QPushButton("Create Maze", self)
        self.createBtn.setFont(FONT3)
        self.createBtn.setFixedHeight(150)

        self.layout.addWidget(info_lbl)
        self.layout.addWidget(maze_lbl)
        self.layout.addWidget(self.loadBtn)
        self.layout.addWidget(self.createBtn)

        #displays a prompt to enter maze dimensions
        create_lbl = QLabel("Enter Maze Dimentions: ")
        create_lbl.setFont(FONT3)
        self.layout.addWidget(create_lbl)
        
        h_layout = QHBoxLayout()
        self.layout.addLayout(h_layout)

        self.entry_box1 = QLineEdit(self)
        self.entry_box1.setValidator(QIntValidator())
        self.entry_box1.setPlaceholderText("Rows")
        self.entry_box1.setFont(FONT3)
        self.entry_box1.setMinimumSize(200, 100)
        h_layout.addWidget(self.entry_box1)

        x_lbl = QLabel("X")
        x_lbl.setFont(FONT3)
        h_layout.addWidget(x_lbl)        

        self.entry_box2 = QLineEdit(self)
        self.entry_box2.setValidator(QIntValidator())
        self.entry_box2.setPlaceholderText("Columns")
        self.entry_box2.setFont(FONT3)
        self.entry_box2.setMinimumSize(200, 100)
        h_layout.addWidget(self.entry_box2)

    #validates maze dimensions and creates a maze
    def createMaze(self):

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
                self.mainWin.startCreateUI((int(self.entry_box1.text()), int(self.entry_box2.text())))

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

