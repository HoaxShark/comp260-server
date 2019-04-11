import socket


class Input:

    def __init__(self, my_socket):
        self.my_socket = my_socket
        self.salt = ''

    def set_salt(self, salt):
        self.salt = salt

    def player_input(self, new_input):
        current_input = new_input  # Get input from player
        # split the player input string
        split_input = current_input.split(' ', 1)
        # stores the first word of the input string (use this across the board)
        first_word = split_input[0].lower()

        if self.my_socket is not None:
            if first_word == 'password':
                # do password salting here
                salted_password = 'username_salt '
                salted_password += split_input[1]
                self.my_socket.send(salted_password.encode())

            # Send normal messages
            else:
                self.my_socket.send(current_input.encode())
