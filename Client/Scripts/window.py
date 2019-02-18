import socket
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from queue import *


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('gui_layout.ui', self)
        self.input_manager = ''
        # queue that holds all messages from the server
        self.messageQueue = Queue()

        # setup for the timer event function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

    def window_draw(self):
        self.ui.show()

    # runs during alongside the window, use as an update function
    def timerEvent(self):
        # while messages in the queue print them to client
        while self.messageQueue.qsize() > 0:
            self.plainTextEdit.appendPlainText(self.messageQueue.get())

    # sends entered text to the input manager if not blank, then clears the text box
    def text_enter(self):
        if self.lineEdit.text() != '':
            self.input_manager.player_input(self.lineEdit.text())
        self.lineEdit.clear()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return:
            self.text_enter()
