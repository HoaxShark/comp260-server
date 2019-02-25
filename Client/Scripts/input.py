import socket


class Input:

    def __init__(self, my_socket):
        self.lowered_input = ''
        self.my_socket = my_socket

    def player_input(self, new_input):
        current_input = new_input  # Get input from player
        self.lowered_input = current_input.lower()  # Transform to lowercase
        try:
            self.my_socket.send(self.lowered_input.encode())
        except socket.error:
            print("Unable to send to serve")
