class Input:
    def __init__(self):
        self.lowered_input = ''  # lowercase version of what was input
        self.current_input = ''  # latest input from the client
        self.all_connected_clients = ''  # dictionary of all current clients
        self.current_client = ''  # the client input is currently being managed for
        # self.players_in_room_names = ''  # the player names of people in the room

    # returns all other clients in the same room
    def check_room_for_players(self, my_player):
        clients_in_room = {}  # all clients in the same room as the player
        for other_client in self.all_connected_clients:
            # get the player attached to the client
            other_player = self.all_connected_clients.get(other_client)
            # if client is in the same room as the player add to the list of clients
            if my_player.current_room == other_player.current_room:
                # check that it isn't the current client we have found
                if other_client != self.current_client:
                    # add other_client to the dict of clients in room
                    clients_in_room[other_client] = 0
                    # self.players_in_room_names += other_player.player_name + ", "
        return clients_in_room

    # tells all players in room that the player has left
    def joined_or_left_room(self, my_player, joined_or_left):
        clients_in_room = self.check_room_for_players(my_player)
        message_to_say = my_player.player_name + " has " + joined_or_left + " the room"
        for client in clients_in_room:
            client.send(message_to_say.encode())

    # shows a full list of possible commands in the game
    def print_help(self):
        return 'Possible commands: \n north - travel north \n east - travel east \n south - travel south' \
               '\n west - travel west \n look - look around current location \n' \
               ' say <text> - talk to everyone in your room \n name <new_name> - rename yourself \n pickup <item_name> - pickup and item in a room\n ' \
               'drop <item_name> - drop item in the room \n equip <item_name> - equip yourself with an item in your inventory \n ' \
               'unequip <item_name> - take off an equipped item and store it in your inventory \n check inventory - see whats in your inventory \n check equipment - see what you have equipped\n'

    # manages all input from clients
    def player_input(self, current_input, client, dungeon):
        self.current_input = current_input  # Get input from player
        self.current_client = client
        self.lowered_input = current_input.lower()  # Transform to lowercase

        my_dungeon = dungeon
        my_player = self.all_connected_clients.get(client)
        # split the player input string
        split_input = current_input.split(' ', 1)
        # stores the first word of the input string (use this across the board)
        first_word = split_input[0].lower()

        #  Exit game if exit is entered
        if self.lowered_input == 'exit':
            # disconnect from server here
            return

        # if trying to talk send message to all other clients in the room
        elif first_word == 'say':
            # pop the first word out of the list
            split_input.pop(0)
            # reform the list into a string
            message_to_say = '<font color="blue">' + my_player.player_name + ': '
            message_to_say += ''.join(split_input) + '</font>'
            # create and send message to input client about what they said
            message_to_yourself = '<font color="dark blue">You say: ' + ''.join(split_input) + '</font>'
            client.send(message_to_yourself.encode())
            # send message to all clients in room
            clients_in_room = self.check_room_for_players(my_player)
            for client in clients_in_room:
                client.send(message_to_say.encode())
            return

        elif first_word == 'name':
            # pop the first word out of the list
            split_input.pop(0)
            if split_input:
                # check that the user entered a name
                if split_input[0] is not '':
                    # rename player
                    my_player.player_name = ''.join(split_input)
                    return 'You are now named: ' + ''.join(split_input)
                else:
                    return 'You must enter a name.'
            else:
                return 'You must enter a name.'

        elif first_word == 'pickup':
            # pop the first word out of the list
            split_input.pop(0)
            # store item name
            item_name = ''.join(split_input)
            # check if that item is in the room
            for item in my_dungeon.rooms[my_player.current_room].items:
                # if item the player is trying to pick up matches the item in a room
                if item_name == item.name.lower():
                    # give that item to the player
                    my_player.inventory[item] = item.name
                    # delete the item from the room
                    del my_dungeon.rooms[my_player.current_room].items[item]
                    # inform the player they got the item
                    return 'You have picked up ' + item_name
            # no matching item was found
            return 'No such item here.'

        elif first_word == 'drop':
            # pop the first word out of the list
            split_input.pop(0)
            # store item name
            item_name = ''.join(split_input)
            # check if that item is in the room
            for item in my_player.inventory:
                # if item the player is trying to pick up matches the item in a room
                if item_name == item.name.lower():
                    # give that item to the room
                    my_dungeon.rooms[my_player.current_room].items[item] = item.name
                    # delete the item from the player
                    del my_player.inventory[item]
                    # inform the player they got the item
                    return 'You have dropped ' + item_name
            # no matching item was found
            return 'No such item in your inventory.'

        elif first_word == 'equip':
            # pop the first word out of the list
            split_input.pop(0)
            # store item name
            item_name = ''.join(split_input)
            return my_player.equip_item(item_name)

        elif first_word == 'unequip':
            # pop the first word out of the list
            split_input.pop(0)
            # store item name
            item_name = ''.join(split_input)
            return my_player.unequip_item(item_name)

        # player can check their inventory or equipment
        elif first_word == 'check':
            # pop the first word out of the list
            split_input.pop(0)
            # store item name
            what_to_check = ''.join(split_input)
            if what_to_check.lower() == "inventory":
                return my_player.check_items("inventory")
            elif what_to_check.lower() == "equipment":
                return my_player.check_items("equipment")
            else:
                return "You can only check your inventory or equipment.\n"

        elif self.lowered_input == 'look':
            all_items = 'Items in room: '
            for item in my_dungeon.rooms[my_player.current_room].items:
                all_items += item.name + '\n'
            if my_dungeon.rooms[my_player.current_room].items:
                return my_dungeon.rooms[my_player.current_room].look_description + '\n' + all_items
            else:
                return my_dungeon.rooms[my_player.current_room].look_description

        #  Move between rooms
        elif self.lowered_input == 'north':
            if my_dungeon.rooms[my_player.current_room].north_connection != '':
                self.joined_or_left_room(my_player, 'left')
                my_player.current_room = my_dungeon.rooms[my_player.current_room].north_connection
                self.joined_or_left_room(my_player, 'joined')
                clients_in_room = self.check_room_for_players(my_player)
                reply_to_player = my_dungeon.rooms[my_player.current_room].description
                if clients_in_room:
                    reply_to_player += "You see - "
                    for client in clients_in_room:
                        reply_to_player += self.all_connected_clients[client].player_name + " - "
                    reply_to_player += "in the room already.\n"

                return reply_to_player
            else:
                return 'There is no path this way'
        elif self.lowered_input == 'east':
            if my_dungeon.rooms[my_player.current_room].east_connection != '':
                self.joined_or_left_room(my_player, 'left')
                my_player.current_room = my_dungeon.rooms[my_player.current_room].east_connection
                self.joined_or_left_room(my_player, 'joined')
                clients_in_room = self.check_room_for_players(my_player)
                reply_to_player = my_dungeon.rooms[my_player.current_room].description
                if clients_in_room:
                    reply_to_player += "You see - "
                    for client in clients_in_room:
                        reply_to_player += self.all_connected_clients[client].player_name + " - "
                    reply_to_player += "in the room already.\n"

                return reply_to_player
            else:
                return 'There is no path this way'
        elif self.lowered_input == 'south':
            if my_dungeon.rooms[my_player.current_room].south_connection != '':
                self.joined_or_left_room(my_player, 'left')
                my_player.current_room = my_dungeon.rooms[my_player.current_room].south_connection
                self.joined_or_left_room(my_player, 'joined')
                clients_in_room = self.check_room_for_players(my_player)
                reply_to_player = my_dungeon.rooms[my_player.current_room].description
                if clients_in_room:
                    reply_to_player += "You see - "
                    for client in clients_in_room:
                        reply_to_player += self.all_connected_clients[client].player_name + " - "
                    reply_to_player += "in the room already.\n"

                return reply_to_player
            else:
                return 'There is no path this way'
        elif self.lowered_input == 'west':
            if my_dungeon.rooms[my_player.current_room].west_connection != '':
                self.joined_or_left_room(my_player, 'left')
                my_player.current_room = my_dungeon.rooms[my_player.current_room].west_connection
                self.joined_or_left_room(my_player, 'joined')
                clients_in_room = self.check_room_for_players(my_player)
                reply_to_player = my_dungeon.rooms[my_player.current_room].description
                if clients_in_room:
                    reply_to_player += "You see - "
                    for client in clients_in_room:
                        reply_to_player += self.all_connected_clients[client].player_name + " - "
                    reply_to_player += "in the room already.\n"

                return reply_to_player
            else:
                return'There is no path this way'

        #  Print list of commands
        elif self.lowered_input == 'help':
            return self.print_help()

        else:
            #  if incorrect input tell user
            return 'No such command - type "help" for a list of commands'
