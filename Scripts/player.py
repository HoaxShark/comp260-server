class Player:

    player_id = ''  # Identification tag of the player
    current_room = ''  # Room the player is currently in
    current_weight = ''  # The current weight of everything the player has
    max_weight = ''  # Maximum weight the player can reach before being unable to move
    inventory = []  # Items the player has on them
    equipped = []  # Items the player had equipped

    def __init__(self, start_room):
        self.current_room = start_room

    def player_input(self):
        current_input = input('Enter Command: ')  # Get input from player
        lowered_input = current_input.lower()  # Transform to lowercase
        print(lowered_input)
        print(self.current_room)
