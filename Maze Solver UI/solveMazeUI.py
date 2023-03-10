from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from algorithms.maze_solver import MazeSolver
from constants import *

# main maze UI
# used for the solve UI
# it can load mazes from files templates passed in
class SolveMazeUI(QWidget):
    def __init__(self, mainWin=None, maze_template=None):
        super(SolveMazeUI, self).__init__(mainWin)

        self.mainWin = mainWin
        self.maze_template = maze_template

        # creating a loop/timer so the illustrate the solution being solved
        self.solution_loop = QTimer(self)
        self.solution_loop.timeout.connect(self.illustrateSolution)

        # fileDialog
        self.fileDialog = QFileDialog()

        # defines rows and cols in maze
        self.rows = len(self.maze_template)
        self.cols = max(len(row) for row in self.maze_template)
        self.initGame()
        self.initLoadUI()

    # function to init variables
    def initGame(self):

        # creating a 2D array of labels
        # each label acts like a cell/position in the maze
        self.cells = [
            [QLabel(self) for i in range(self.cols)] for j in range(self.rows)
        ]

        # calls method to init Maze UI
        self.mainWin.initMaze(cells=self.cells, maze_template=self.maze_template)

    # solves maze
    def solveMaze(self):

        # resetting maze to it's unsolved state
        self.mainWin.resetMaze(self.cells, self.maze_template)
        # this block ensures that the user spamming the solve button will not have any unintended consequences
        try:
            self.solution_loop.stop()
        except:
            pass

        # getting method to be used
        if self.a_star_btn.isChecked():
            method = "A* Search"
        elif self.bfs_btn.isChecked():
            method = "Breadth First Search"
        else:
            method = "Depth First Search"

        maze_solver = MazeSolver()
        # returns output (None = no start or end node). 1 == ok
        output = maze_solver.parse_maze(self.maze_template)

        if output is not None:
            # Note: The explored states also contain the solution states
            # func can also return None, None (which means there is no solution)
            self.solution, self.explored = maze_solver.solve_maze(method)

        try:
            # removing last state from solution since it is the goal state
            self.solution.pop()
            # removing first state from explored since it is the start state
            self.explored.pop(0)

            # display_solution will contain all the states that need to be displayed(explored and/or solution states)
            if self.show_explored_checkBox.isChecked():
                self.display_solution = self.explored
            else:
                self.display_solution = self.solution

            # using user specified speed
            self.solution_loop.start(
                self.speed_slider.maximum() - self.speed_slider.value()
            )

            self.index = 0
            self.solution_states = 0
            self.explored_states = 0

        # if there is no solution or the starting/ending node is not in the maze
        except:
            if output is None:
                self.mainWin.showWarning("No start/end node in maze")
            else:
                self.mainWin.showWarning("This maze has no solution")

    # a looped function that is used to illustrate the maze being solved
    def illustrateSolution(self):

        explored_cell_x, explored_cell_y = self.display_solution[self.index]

        # finding the cell that corresponds to the explored state in display_solution
        cell = self.cells[explored_cell_x][explored_cell_y]
        # setting cell green if it is a solution state and yellow if it is just an explored state
        if (explored_cell_x, explored_cell_y) in self.solution:
            cell.setStyleSheet(STYLE1 + GREEN)
            self.solution_states += 1
            self.explored_states += 1
        else:
            cell.setStyleSheet(STYLE1 + YELLOW)
            self.explored_states += 1

        self.index += 1
        if self.index == len(self.display_solution):

            # ending loop and setting explored states to actual
            self.explored_states = len(self.explored)
            self.index = 0
            self.solution_loop.stop()

        # updating maze stats
        self.solution_states_lbl.setText(
            "Solution States: " + str(self.solution_states)
        )
        self.explored_states_lbl.setText(
            "States Explored: " + str(self.explored_states)
        )
        
    # UI for maze solving
    def initLoadUI(self):
        # widgets above the maze grid

        # solving method buttons
        radio_widget = QWidget(self)
        radio_widget.setMinimumSize(550, MAZE_CTRL_SPACING)
        radio_widget.move(0, -10)
        radio_widget.setFont(FONT1)
        radio_layout = QVBoxLayout(radio_widget)

        self.a_star_btn = QRadioButton("A* Search    ", radio_widget)
        self.a_star_btn.setChecked(True)
        self.bfs_btn = QRadioButton("Breadth First Search    ", radio_widget)
        self.dfs_btn = QRadioButton("Depth First Search    ", radio_widget)

        # checkbox for explored states
        self.show_explored_checkBox = QCheckBox("Visualize", radio_widget)

        radio_layout.addWidget(self.a_star_btn)
        radio_layout.addWidget(self.bfs_btn)
        radio_layout.addWidget(self.dfs_btn)
        radio_layout.addWidget(self.show_explored_checkBox)

        # ------------------------------------solve layout------------------------------------#
        solve_widget = QWidget(self)
        solve_widget.setFont(FONT1)
        solve_widget.move(400, -10)
        solve_main_layout = QVBoxLayout(solve_widget)

        solve_Hlayout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setFixedSize(200, 50)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(150)

        self.speed_label = QLabel("Speed: " + str(self.speed_slider.value()), self)
        self.speed_label.setFixedSize(175, 50)

        self.speed_slider.valueChanged.connect(
            lambda: self.speed_label.setText(
                "Speed: " + str(self.speed_slider.value()) + "   "
            )
        )

        # solve button (inside same widget as speed slider)
        solve_btn = QPushButton("Solve maze", self)
        solve_btn.setFont(FONT1)
        solve_btn.setMaximumHeight(130)
        solve_btn.setStyleSheet("background-color: " + GREEN)
        solve_btn.clicked.connect(self.solveMaze)

        # save and edit buttons
        save_edit_Vlayout = QVBoxLayout()
        save_btn = QPushButton("Save maze", self)
        save_btn.setFont(FONT1)
        save_btn.setMaximumHeight(60)
        save_btn.setStyleSheet("background-color: " + ORANGE + "; color: " + WHITE)
        save_btn.clicked.connect(lambda: self.mainWin.saveMaze(self.cells))

        edit_btn = QPushButton("Edit maze", self)
        edit_btn.setFont(FONT1)
        edit_btn.setMaximumHeight(60)
        edit_btn.setStyleSheet("background-color: " + YELLOW)
        edit_btn.clicked.connect(
            lambda: self.mainWin.startCreateUI(maze_template=self.maze_template)
        )

        # main menu button
        menu_btn = QPushButton("New maze", self)
        menu_btn.setMinimumHeight(85)
        menu_btn.setStyleSheet("background-color: " + BLUE + "; color: " + WHITE)
        menu_btn.clicked.connect(lambda: self.mainWin.startStartUpUI())
        menu_btn.setFont(FONT1)

        # maze statistics
        stats_widget = QWidget(self)
        stats_widget.setFont(FONT1)
        stats_widget.move(400, 115)
        stats_layout = QVBoxLayout(stats_widget)

        self.solution_states_lbl = QLabel("Solution States: 0", stats_widget)
        self.solution_states_lbl.setMinimumWidth(350)

        self.explored_states_lbl = QLabel("States Explored: 0", stats_widget)
        self.explored_states_lbl.setMinimumWidth(350)

        solve_Vlayout = QVBoxLayout()
        spacer_Hlayout = QHBoxLayout()

        stats_layout.addWidget(self.solution_states_lbl)
        stats_layout.addWidget(self.explored_states_lbl)

        save_edit_Vlayout.addWidget(save_btn)
        save_edit_Vlayout.addWidget(edit_btn)

        solve_Hlayout.addWidget(self.speed_label)
        solve_Hlayout.addWidget(self.speed_slider)
        solve_Hlayout.addWidget(solve_btn)
        solve_Hlayout.addLayout(save_edit_Vlayout)

        solve_Vlayout.addLayout(solve_Hlayout)
        spacer_Hlayout.addSpacing(405)
        spacer_Hlayout.addWidget(menu_btn)
        solve_Vlayout.addLayout(spacer_Hlayout)

        solve_main_layout.addLayout(solve_Vlayout)
