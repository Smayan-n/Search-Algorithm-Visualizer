from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, time

class Slider(QSlider):
    minimumChanged = QtCore.signal(int)
    maximumChanged = QtCore.signal(int)

    def setMinimum(self, minimum):
        self.minimumChanged.emit(minimum)
        super(Slider, self).setMinimum(minimum)

    def setMaximum(self, maximum):
        self.maximumChanged.emit(maximum)
        super(Slider, self).setMaximum(maximum)

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(alignment=QtCore.Qt.AlignCenter)

        self.slider = Slider(tickPosition=QSlider.TicksLeft,
            orientation=QtCore.Qt.Horizontal)
        slider_vbox = QVBoxLayout()
        slider_hbox = QHBoxLayout()
        slider_hbox.setContentsMargins(0, 0, 0, 0)
        slider_vbox.setContentsMargins(0, 0, 0, 0)
        slider_vbox.setSpacing(0)
        label_minimum = QLabel(alignment=QtCore.Qt.AlignLeft)
        self.slider.minimumChanged.connect(label_minimum.setNum)
        label_maximum = QLabel(alignment=QtCore.Qt.AlignRight)
        self.slider.maximumChanged.connect(label_maximum.setNum)
        slider_vbox.addWidget(self.slider)
        slider_vbox.addLayout(slider_hbox)
        slider_hbox.addWidget(label_minimum, QtCore.Qt.AlignLeft)
        slider_hbox.addWidget(label_maximum, QtCore.Qt.AlignRight)
        slider_vbox.addStretch()

        self.slider.setMinimum(0)
        self.slider.setMaximum(100)

        vbox = QVBoxLayout(self)
        vbox.addLayout(slider_vbox)
        vbox.addWidget(self.label)
        self.setGeometry(300, 300, 300, 150)
        self.slider.valueChanged.connect(self.label.setNum)
        self.show()

def main():    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()