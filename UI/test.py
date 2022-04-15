from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random, sys


class MyApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Group Checkbox with QGroupBox Widget')
		self.setMinimumWidth(600)

		layout = QVBoxLayout()
		self.setLayout(layout)

		groupBox = QGroupBox('My GroupBox')
		groupBox.setCheckable(True)
		layout.addWidget(groupBox)

		groupBoxLayout = QVBoxLayout()
		groupBox.setLayout(groupBoxLayout)

		for i in range(5):
			groupBoxLayout.addWidget(QRadioButton('Checkbox {0}'.format(i)))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			font-size: 35px;
		}
	''')
	
	myApp = MyApp()
	myApp.show()

	try:
		sys.exit(app.exec_())
	except SystemExit:
		print('Closing Window...')