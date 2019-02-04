class Input:
    def __init__(self):
        self.number_incorrect_inputs: int = 0  # track consecutive incorrect inputs
        self.lowered_input: str = ''  # lowercase version of what was input
        self.current_input: str = ''  # latest input from the client

    # shows a full list of possible commands in the game
    def print_help(self):
        return 'Possible commands: \n north - travel north \n east - travel east \n south - travel south' \
               '\n west - travel west \n look - look around current location \n exit - exit the game'

    # manages all input from clients
    def player_input(self, current_input, player, dungeon):
        self.current_input = current_input  # Get input from player
        my_dungeon = dungeon
        my_player = player

        #  Exit game if exit is entered
        if self.current_input == 'exit':
            # disconnect from server here
            return

        elif self.current_input == 'look':
            return my_dungeon.rooms[my_player.current_room].look_description

        #  Move between rooms
        elif self.current_input == 'north':
            if my_dungeon.rooms[my_player.current_room].north_connection != '':
                my_player.current_room = my_dungeon.rooms[my_player.current_room].north_connection
                return my_dungeon.rooms[my_player.current_room].description
            else:
                return 'There is no path this way'
        elif self.current_input == 'east':
            if my_dungeon.rooms[my_player.current_room].east_connection != '':
                my_player.current_room = my_dungeon.rooms[my_player.current_room].east_connection
                return my_dungeon.rooms[my_player.current_room].description
            else:
                return 'There is no path this way'
        elif self.current_input == 'south':
            if my_dungeon.rooms[my_player.current_room].south_connection != '':
                my_player.current_room = my_dungeon.rooms[my_player.current_room].south_connection
                return my_dungeon.rooms[my_player.current_room].description
            else:
                return 'There is no path this way'
        elif self.current_input == 'west':
            if my_dungeon.rooms[my_player.current_room].west_connection != '':
                my_player.current_room = my_dungeon.rooms[my_player.current_room].west_connection
                return my_dungeon.rooms[my_player.current_room].description
            else:
                return'There is no path this way'

        #  Print list of commands
        elif self.current_input == 'help':
            return self.print_help()

        else:
            #  if incorrect input tell user
            if self.number_incorrect_inputs <= 5:
                self.number_incorrect_inputs += 1
                return 'No such command - type "help" for a list of commands'

            #  if incorrect too many times in a row print the possible commands
            else:
                help_text = 'Ok dont worry, I will do it for you :) \n'
                help_text += self.print_help()
                return help_text

        self.number_incorrect_inputs = 0  # if a correct input is entered reset counter
