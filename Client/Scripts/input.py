class Input:

    def __init__(self):
        self.lowered_input = ''

    def player_input(self):
        current_input = input('Enter Command: ')  # Get input from player
        self.lowered_input = current_input.lower()  # Transform to lowercase
