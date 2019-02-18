import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets, uic


class Window(QtWidgets.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('gui_layout.ui', self)
        self.setGeometry(50,50,500,500)
        self.setWindowTitle("The best MUD")
        #self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

    def window_draw(self):
        self.show()