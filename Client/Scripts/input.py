import socket
import bcrypt

class Input:

    def __init__(self, my_socket):
        self.my_socket = my_socket
        self.salt = ''
        self.password = ''
        self.username = ''

    def set_salt(self, salt):
        self.salt = salt

    def set_username_password(self, username, password):
        self.username = username
        self.password = password

    def send_username(self):
        message = '#username ' + self.username
        self.my_socket.send(message.encode())

    def send_password(self):
        # Encode password and salt
        self.password = self.password.encode('utf-8')
        self.salt = self.salt.encode('utf-8')
        # Hash password
        self.password = bcrypt.hashpw(self.password, self.salt)
        # Decode password
        self.password = self.password.decode()
        message = '#username_salt ' + self.password
        self.my_socket.send(message.encode())

    def player_input(self, new_input):
        current_input = new_input  # Get input from player
        # split the player input string
        split_input = current_input.split(' ', 1)
        # stores the first word of the input string (use this across the board)
        first_word = split_input[0].lower()

        if self.my_socket is not None:
            self.my_socket.send(current_input.encode())
