from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from queue import *


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('gui_layout.ui', self)
        self.input_manager = ''
        # queue that holds all messages from the server
        self.message_queue = Queue()

        # setup for the timer event function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)
        self.client = ''
        self.salt = ''
        self.logged_in = False

    def set_logged_in(self, logged_in):
        self.logged_in = logged_in

    def window_draw(self):
        self.ui.show()

    # runs during alongside the window, use as an update function
    def timerEvent(self):
        # while messages in the queue print them to client
        while self.message_queue.qsize() > 0:
            current_input = self.message_queue.get()  # Get messege out the queue
            # split the player input string
            split_input = current_input.split(' ', 1)
            # stores the first word of the input string (use this across the board)
            first_word = split_input[0].lower()

            if first_word == 'username_salt':
                self.salt = split_input[1]
                self.input_manager.set_salt(self.salt)
            elif first_word == 'login_accepted':
                self.logged_in = True
            else:
                self.textEdit.append(current_input)

    # sends entered text to the input manager if not blank, then clears the text box
    def text_enter(self):
        if self.lineEdit.text() != '':
            self.input_manager.player_input(self.lineEdit.text())
        self.lineEdit.clear()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return:
            self.text_enter()

    # runs when the pyqt window is closed, shuts down the client and ends current threads
    def closeEvent(self, event):
        self.client.is_running = False
        self.client.is_connected = False

        self.client.my_socket.close()
        self.client.my_socket = None

        if self.client.my_receive_thread is not None:
            self.client.my_receive_thread.join
        if self.client.my_connection_thread is not None:
            self.client.my_connection_thread.join

    def set_client(self, this_client):
        self.client = this_client
