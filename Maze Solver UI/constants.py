#file to store all global constants for maze UI app

from PyQt5.QtGui import QFont

FONT1 = QFont("Aerial", 10)
FONT2 = QFont("Aerial", 12)
FONT3 = QFont("Aerial", 15)

#colors
BG_COLOR = "rgb(100, 100, 100)"
GREEN = "rgb(0, 200, 0)"
GREY = "rgb(100, 100, 100)"
RED = "rgb(200, 0, 0)"
BLUE = "rgb(0, 0, 200)"
WHITE = "rgb(255, 255, 255)"
YELLOW = "rgb(255, 255, 0)"
ORANGE = "rgb(200, 100, 0)"

#styles
STYLE1 = "border: 1px solid black; background-color: "

#maze constants

#dimension of each cell in the maze (square)
MAZE_CELL_SIZE = 60
#space for buttons and controls above the maze
MAZE_CTRL_SPACING = 250

MIN_WIN_WIDTH = 1250