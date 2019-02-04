class Player:

    def __init__(self, dungeon, start_room):
        self.current_room: str = start_room  # Room the player is currently in
        self.game_running: bool = True  # if the game is still running or not
        self.dungeon_ref = dungeon  # The entire dungeon
        self.player_id: int = 0  # Identification tag of the player
        self.current_weight: int = 0  # The current weight of everything the player has
        self.max_weight: int  # Maximum weight the player can reach before being unable to move
        self.inventory = {}  # Items the player has on them
        self.equipped = {}  # Items the player had equipped
        self.number_incorrect_inputs: int = 0  # track consecutive incorrect inputs

        # Intro for the player
        print('You have made it to the hallway, finally, but can you really go through the doors?')
        print(self.dungeon_ref.rooms[self.current_room].description)

    def print_help(self):
        print('Possible commands:')
        print('north - travel north')
        print('east - travel east')
        print('south - travel south')
        print('west - travel west')
        print('look - look around current location')
        print('exit - exit the game')

    def player_input(self):
        current_input = input('Enter Command: ')  # Get input from player
        lowered_input = current_input.lower()  # Transform to lowercase

        #  Exit game if exit is entered
        if lowered_input == 'exit':
            self.game_running = False
            return

        elif lowered_input == 'look':
            print(self.dungeon_ref.rooms[self.current_room].look_description)

        #  Move between rooms
        elif lowered_input == 'north':
            if self.dungeon_ref.rooms[self.current_room].north_connection != 'none':
                self.current_room = self.dungeon_ref.rooms[self.current_room].north_connection
                print(self.dungeon_ref.rooms[self.current_room].description)
            else:
                print('There is no path this way')
        elif lowered_input == 'east':
            if self.dungeon_ref.rooms[self.current_room].east_connection != 'none':
                self.current_room = self.dungeon_ref.rooms[self.current_room].east_connection
                print(self.dungeon_ref.rooms[self.current_room].description)
            else:
                print('There is no path this way')
        elif lowered_input == 'south':
            if self.dungeon_ref.rooms[self.current_room].south_connection != 'none':
                self.current_room = self.dungeon_ref.rooms[self.current_room].south_connection
                print(self.dungeon_ref.rooms[self.current_room].description)
            else:
                print('There is no path this way')
        elif lowered_input == 'west':
            if self.dungeon_ref.rooms[self.current_room].west_connection != 'none':
                self.current_room = self.dungeon_ref.rooms[self.current_room].west_connection
                print(self.dungeon_ref.rooms[self.current_room].description)
            else:
                print('There is no path this way')

        #  Print list of commands
        elif lowered_input == 'help':
            self.print_help()

        else:
            #  if incorrect input tell user
            if self.number_incorrect_inputs <= 5:
                print('No such command - type "help" for a list of commands')
                self.number_incorrect_inputs += 1
                return
            #  if incorrect too many times in a row print the possible commands
            else:
                print('Ok dont worry, I will do it for you :)')
                self.print_help()

        self.number_incorrect_inputs = 0  # if a correct input is entered reset counter


