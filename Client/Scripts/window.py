import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50,50,500,500)
        self.setWindowTitle("The best MUD")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

    def window_draw(self):
        self.show()