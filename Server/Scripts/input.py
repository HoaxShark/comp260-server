from Scripts import database
import json

from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Input:
    def __init__(self):
        self.lowered_input = ''  # lowercase version of what was input
        self.current_input = ''  # latest input from the client
        self.all_connected_clients = {}  # dictionary of all current clients
        self.current_client = ''  # the client input is currently being managed for
        self.db = database.Database()  # database reference
        self.clients_login_area = []  # Stores users able to access login commands
        self.clients_play_area = []  # Stores users able to access play commands
        self.logged_in_users = {}  # Dictionary of all users that are logged in
        self.packet_id = 'BestMUD'  # Used to confirm to the server that the incoming packets should be read
        self.setup_packet_id = 'Setup!!'  # Used to tell the client this message contains setup info
        self.encryption_key = ''  # 16 bit key used for encryption

    # Allows main to add newly connected clients to the login area
    def add_client_to_login_area(self, client):
        self.clients_login_area.append(client)

    # Used to clear a client from lists if they lose connection
    def clear_client_from_lists(self, client):
        if client in self.clients_login_area:
            self.clients_login_area.remove(client)
        if client in self.clients_play_area:
            self.clients_play_area.remove(client)
        if client in self.logged_in_users:
            del self.logged_in_users[client]

    # returns all other clients in the same room
    def check_room_for_players(self, my_player):
        clients_in_room = {}  # all clients in the same room as the player
        for other_client in self.all_connected_clients:
            # get the player attached to the client
            other_player = self.all_connected_clients.get(other_client)
            # if client is in the same room as the player add to the list of clients
            if self.db.get_current_room(my_player) == self.db.get_current_room(other_player):
                # check that it isn't the current client we have found
                if other_client != self.current_client:
                    # add other_client to the dict of clients in room
                    clients_in_room[other_client] = 0
        return clients_in_room

    # tells all players in room that the player has left
    def joined_or_left_room(self, my_player, joined_or_left):
        clients_in_room = self.check_room_for_players(my_player)
        message_to_say = my_player + " has " + joined_or_left + " the room"
        for client in clients_in_room:
            self.send_message(message_to_say, client)

    # Send encrypted message to client
    def send_message(self, message, client):
        # Create cipher for the encrypted message
        cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        # Encrypt message into bytes
        ciphertext_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        # Extract the initialisation vector
        iv = b64encode(cipher.iv).decode('utf-8')
        ciphertext = b64encode(ciphertext_bytes).decode('utf-8')
        json_message = json.dumps({'iv': iv, 'ciphertext': ciphertext})

        # Header used to inform the server of the upcoming packet size
        header = len(json_message).to_bytes(2, byteorder='little')

        if client is not None:
            # Send all required information to the server
            client.send(self.packet_id.encode())
            client.send(header)
            client.send(json_message.encode())

    # Send the initial setup message with the encryption key
    def send_setup_info(self, key, client):
        key = b64encode(key).decode('utf-8')  # key.decode()
        # Dictionary of information to send to the server, room to expand
        my_dict = {'key': key}
        # Transform dictionary into json
        json_packet = json.dumps(my_dict)
        # Header used to inform the server of the upcoming packet size
        header = len(json_packet).to_bytes(2, byteorder='little')

        if self.current_client is not None:
            # Send all required information to the server
            client.send(self.setup_packet_id.encode())
            client.send(header)
            client.send(json_packet.encode())

    # shows a full list of possible commands in the game
    def print_help(self):
        return 'Possible commands: \n north - travel north \n east - travel east \n south - travel south' \
               '\n west - travel west \n look - look around current location \n' \
               ' say <text> - talk to everyone in your room \n pickup <item_name> - pickup and item in a room\n ' \
               'drop <item_name> - drop item in the room \n check inventory - see whats in your inventory \n'

    def move_room(self, direction, my_player):
        # Get the players current_room
        current_room = self.db.get_current_room(my_player)
        # Get the connected room in the given direction
        connection_id = self.db.get_connection(direction, current_room)
        if connection_id != 0:
            self.joined_or_left_room(my_player, 'left')
            # Update current room
            self.db.set_current_room(my_player, connection_id)
            self.joined_or_left_room(my_player, 'joined')
            clients_in_room = self.check_room_for_players(my_player)
            reply_to_player = self.db.get_value('dungeon', 'base_description', 'room_id', connection_id)
            if clients_in_room:
                reply_to_player += "You see - "
                for client in clients_in_room:
                    reply_to_player += self.all_connected_clients[client] + " - "
                reply_to_player += "in the room already.\n"

            return reply_to_player
        else:
            return 'There is no path this way'

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

        # If client is in the login area they can then access the login commands
        elif client in self.clients_login_area:

            # if receiving username_login. username_login, username, password
            if first_word == '#username':
                # pop the first word out of the list
                split_input.pop(0)
                # check the username exists
                exists = self.db.check_value('users', 'username', split_input[0], 'username', split_input[0])
                if exists:
                    already_logged_in = False
                    for client_info, username in self.logged_in_users.items():
                        if username == split_input[0]:
                            already_logged_in = True
                    if already_logged_in:
                        message = 'This user is already logged in'
                        self.send_message(message, client)
                    else:
                        salt = '#username_salt '
                        salt += self.db.get_value('users', 'salt', 'username', split_input[0])
                        # Assign the username to the client
                        self.all_connected_clients[client] = split_input[0]
                        self.send_message(salt, client)
                else:
                    message = 'Username does not exist'
                    self.send_message(message, client)

            # Check password for user
            elif first_word == '#username_salt':
                # pop the first word out of the list
                split_input.pop(0)
                # check the password is correct
                password_correct = self.db.check_value('users', 'password', split_input[0], 'username', my_player)
                if password_correct:
                    # Tell the client that the login has been accepted
                    login_accepted = '#login_accepted'
                    self.send_message(login_accepted, client)
                    # Tell user they have logged in
                    message = 'You have logged in.\n'
                    self.send_message(message, client)
                    # Assign client info and username to the logged in clients dictionary
                    self.logged_in_users[client] = my_player
                    players = self.db.get_all_values('players', 'player_name', 'owner_username', my_player)
                    message = 'Please pick a character: \n - '
                    while len(players) is not 0:
                        message += players[0][0] + ' - '
                        players.pop(0)
                    message += '\n Type select and then the character name. \n Or type create then a character name to make a new character.\n'
                    self.send_message(message, client)
                else:
                    message = 'Password incorrect. \n'
                    self.send_message(message, client)
                    # Reset the username as the password was wrong
                    self.all_connected_clients[client] = 0

            # Create new account, format: username password salt
            # This is called automatically by the client once the user gets past the initial account creation step
            # Receives the username and hashed password from the user to be stored in the database
            elif first_word == '#create_account':
                split_input.pop(0)
                # split the username and password
                split_input = split_input[0].split(' ')
                username = split_input[0]
                password = split_input[1]
                salt = split_input[2]
                exists = self.db.check_value('users', 'username', username, 'username', username)
                if exists:
                    message = 'Username already taken \n'
                    self.send_message(message, client)
                else:
                    self.db.add_user(username, password, salt)
                    message = 'User added, please log in. \n'
                    self.send_message(message, client)

            # Create new account, format: username password salt
            # Check the account name doesn't already exist, if it does tell the user and cancel creation
            # If it doesn't then create the new account
            elif first_word == 'create':
                split_input.pop(0)
                exists = self.db.check_value('players', 'player_name', split_input[0], 'player_name', split_input[0])
                if exists:
                    message = 'Player name already taken \n'
                    self.send_message(message, client)
                else:
                    self.db.add_player(my_player, split_input[0])
                    message = 'Player added, please use select then player name. \n'
                    self.send_message(message, client)

            # User trying to select a player, checks selected name vs all players that the user owns
            # if they own the player then apply that name to them and move them into the play area
            elif first_word == 'select':
                split_input.pop(0)
                player_is_owned = False
                # Get all players owned by the user
                owned_players = self.db.get_all_values('players', 'player_name', 'owner_username', my_player)
                # Check all owned players against the log in
                while len(owned_players) is not 0:
                    if owned_players[0][0] == split_input[0]:
                        player_is_owned = True
                    owned_players.pop(0)
                # If they own the player give them control and inform the user
                if player_is_owned:
                    # Update client to player name
                    self.all_connected_clients[client] = split_input[0]
                    # Add client to play area
                    self.clients_play_area.append(self.current_client)
                    # Remove client from login area
                    self.clients_login_area.remove(self.current_client)
                    message = 'Logged in as ' + split_input[0]
                    self.send_message(message, client)
                    message = 'Type help to view a list of all commands!'
                    self.send_message(message, client)
                # If they don't own the player tell them
                else:
                    message = 'You do not own a character called ' + split_input[0]
                    self.send_message(message, client)

        # If client is in the play area they can then access the play commands
        elif client in self.clients_play_area:

            # If trying to talk send message to all other clients in the room and let the player know what they said
            if first_word == 'say':
                split_input.pop(0)
                # reform the list into a string
                message_to_say = '<font color="blue">' + my_player + ': '
                message_to_say += ''.join(split_input) + '</font>'
                message_to_yourself = '<font color="dark blue">You say: ' + ''.join(split_input) + '</font>'
                self.send_message(message_to_yourself, client)
                # send message to all clients in room
                clients_in_room = self.check_room_for_players(my_player)
                for client in clients_in_room:
                    self.send_message(message_to_say, client)
                return

            elif first_word == 'pickup':
                # pop the first word out of the list
                split_input.pop(0)
                # store item name
                item_name = ''.join(split_input)
                # Get the current room
                current_room = self.db.get_current_room(my_player)
                # Pickup the item
                reply = self.db.pickup_item(item_name, my_player, current_room)
                return reply

            elif first_word == 'drop':
                # pop the first word out of the list
                split_input.pop(0)
                # store item name
                item_name = ''.join(split_input)
                # Get the current room
                current_room = self.db.get_current_room(my_player)
                # Pickup the item
                reply = self.db.drop_item(item_name, my_player, current_room)
                return reply

            # Player check their inventory, lists all items the player has or tells them they have no items
            elif first_word == 'check':
                split_input.pop(0)
                what_to_check = ''.join(split_input)
                if what_to_check.lower() == "inventory":
                    all_items = self.db.get_all_items_in_inventory(my_player)
                    if all_items != None:
                        reply = 'You have: '
                        reply += self.db.get_all_items_in_inventory(my_player) + '\n'
                        return reply
                    else:
                        return "You have no items.\n"
                else:
                    return "You can only check your inventory.\n"

            # Get the detailed room description and check the room for any items, if they exist add this information to the player reply
            elif self.lowered_input == 'look':
                current_room = self.db.get_current_room(my_player)

                if self.db.get_all_items_in_room(current_room) != None:
                    all_items = 'Items in room: '
                    all_items += self.db.get_all_items_in_room(current_room) + '\n'
                    reply_to_player = self.db.get_value('dungeon', 'detailed_description', 'room_id', current_room) + '\n' + all_items
                    return reply_to_player
                else:
                    reply_to_player = self.db.get_value('dungeon', 'detailed_description', 'room_id', current_room)
                    return reply_to_player

            #  Move between rooms depending on the direction given by player
            elif self.lowered_input == 'north':
                return self.move_room('north', my_player) + '\n'

            elif self.lowered_input == 'east':
                return self.move_room('east', my_player) + '\n'

            elif self.lowered_input == 'south':
                return self.move_room('south', my_player) + '\n'

            elif self.lowered_input == 'west':
                return self.move_room('west', my_player) + '\n'

            #  Print list of commands
            elif self.lowered_input == 'help':
                return self.print_help()

        # If no commands match at all
        else:
            return 'No such command - type "help" for a list of commands'
