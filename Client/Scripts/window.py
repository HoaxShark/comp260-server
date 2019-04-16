from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from queue import *

import bcrypt


class LoginWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.login_widget = uic.loadUi('login_widget_layout.ui', self)

        # Center
        self.move(parent.rect().center() - self.rect().center())

        # Set up login window buttons
        self.login_widget.login_button.clicked.connect(parent.login_clicked)
        self.login_widget.create_account_button.clicked.connect(parent.create_account_clicked)


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
        self.connected = False

        self.username = ''
        self.password = ''

        self.login_widget = LoginWidget(self)

    def create_account_clicked(self):
        # Set username and password
        self.username = self.login_widget.username_lineEdit.text()
        self.password = self.login_widget.password_lineEdit.text()

        # Generate the salt for a new account
        salt = bcrypt.gensalt(12)
        # Encode password
        self.password = self.password.encode('utf-8')
        # Hash password
        self.password = bcrypt.hashpw(self.password, salt)
        # Decode password
        self.password = self.password.decode()
        # Decode salt
        salt = salt.decode()

        # Clear widget input lines
        self.login_widget.username_lineEdit.clear()
        self.login_widget.password_lineEdit.clear()

        # Form message and send using input manager
        message = '#create_account ' + self.username + ' ' + self.password + ' ' + salt
        self.input_manager.player_input(message)

    def login_clicked(self):
        # Set username and password
        self.username = self.login_widget.username_lineEdit.text()
        self.password = self.login_widget.password_lineEdit.text()

        # Send over to the input manager
        self.input_manager.set_username_password(self.username, self.password)

        # Clear widget input lines
        self.login_widget.username_lineEdit.clear()
        self.login_widget.password_lineEdit.clear()

        # Tell input manager to send username to the server
        self.input_manager.send_username()

    def set_logged_in(self, logged_in):
        self.logged_in = logged_in

    def set_connected(self, connected):
        self.connected = connected

    def window_draw(self):
        self.ui.show()
        self.login_widget.close()

    # runs during alongside the window, use as an update function
    def timerEvent(self):
        # If not logged in display the log in widget
        if self.logged_in == False and self.connected == True:
            self.login_widget.show()
        else:
            self.login_widget.close()

        # while messages in the queue print them to client
        while self.message_queue.qsize() > 0:
            current_input = self.message_queue.get()  # Get messege out the queue
            # split the player input string
            split_input = current_input.split(' ', 1)
            # stores the first word of the input string (use this across the board)
            first_word = split_input[0].lower()

            if first_word == '#username_salt':
                self.salt = split_input[1]
                # Set salt
                self.input_manager.set_salt(self.salt)
                # Tell input manager to salt and send password
                self.input_manager.send_password()

            elif first_word == '#login_accepted':
                self.logged_in = True
                self.login_widget.close()

            else:
                self.textEdit.append(current_input)

    # sends entered text to the input manager if not blank, then clears the text box
    def text_enter(self):
        if self.lineEdit.text() != '' and self.logged_in:
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
