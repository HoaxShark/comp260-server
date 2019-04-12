import socket


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
        # SALT PASSWORD HERE AND SEND
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
