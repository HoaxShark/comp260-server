class Player:

    current_room = ''

    def __init__(self, start_room):
        self.current_room = start_room

    def player_input(self):
        current_input = input('Enter Command: ')  # Get input from player
        lowered_input = current_input.lower()  # Transform to lowercase
        print(lowered_input)
        print(self.current_room)
