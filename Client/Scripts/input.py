class Input:

    def __init__(self, my_socket):
        self.lowered_input = ''
        self.my_socket = my_socket

    def player_input(self):
        current_input = input('Enter Command: ')  # Get input from player
        self.lowered_input = current_input.lower()  # Transform to lowercase
