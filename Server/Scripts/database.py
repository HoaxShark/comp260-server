import sqlite3


class Database:

    def __init__(self):
        # create or open a file called my_db
        self.db = sqlite3.connect('server_db')
        # get cursor object
        self.cursor = self.db.cursor()
        # Create tables if not already created
        self.create_dungeon_table()
        self.create_player_table()
        self.create_user_table()
        self.create_item_table()

    # Adds a new user to the db
    def add_user(self, username, password, salt):
        # Insert user
        self.cursor.execute('''INSERT INTO users(username, password, salt)
                          VALUES(?,?,?)''', (username, password, salt))
        self.db.commit()
        print('User created')

    # Adds a new player to the db
    def add_player(self, username, player_name):
        # Insert user
        self.cursor.execute('''INSERT INTO players(owner_username, player_name)
                          VALUES(?,?)''', (username, player_name))
        self.db.commit()
        print('Player created')

    # Returns the value of the requested field in a table
    def get_value(self, table_name, field_to_check, query_field, query_value):
        self.cursor.execute('SELECT ' + field_to_check + ' FROM ' + table_name + ' WHERE ' + query_field + ' = ?',
                            (query_value,))
        result = self.cursor.fetchone()  # retrieve the first row
        return result[0]

    # Returns the value of the requested field in a table
    def get_all_values(self, table_name, field_to_check, query_field, query_value):
        self.cursor.execute('SELECT ' + field_to_check + ' FROM ' + table_name + ' WHERE ' + query_field + ' = ?',
                            (query_value,))
        result = self.cursor.fetchall()  # retrieve the first row
        return result

    # Checks the db for a matching value returns False if it doesn't match and True if it does
    def check_value(self, table_name, field_to_check, value_to_check, query_field, query_value):
        self.cursor.execute('SELECT ' + field_to_check + ' FROM ' + table_name + ' WHERE ' + query_field + ' = ?',
                            (query_value,))
        result = self.cursor.fetchone()  # retrieve the first row
        if result != None:
            if result[0] == value_to_check:
                return True
            elif result[0] != value_to_check:
                return False
        else:
            return False

    # Gets the connection from the current room
    def get_connection(self, connection_direction, current_room):
        self.cursor.execute('SELECT ' + connection_direction + ' FROM dungeon WHERE room_id = ?',
                            (current_room,))
        result = self.cursor.fetchone()  # retrieve the first row
        return result[0]

    # Gets the players current room
    def get_current_room(self, my_player):
        self.cursor.execute('SELECT current_room FROM players WHERE player_name = ?',
                            (my_player,))
        result = self.cursor.fetchone()  # retrieve the first row
        # check result is not none
        if result is not None:
            return result[0]
        else:
            return 0

    # Gets the items name
    def get_item_name(self, item_id):
        self.cursor.execute('SELECT item_name FROM items WHERE item_id = ?',
                            (item_id,))
        result = self.cursor.fetchone()  # retrieve the first row
        # check result is not none
        if result is not None:
            return result[0]
        else:
            return

    # Gets the items id
    def get_item_id(self, item_name):
        self.cursor.execute('SELECT item_id FROM items WHERE item_name = ?',
                            (item_name,))
        result = self.cursor.fetchone()  # retrieve the first row
        # check result is not none
        if result is not None:
            return result[0]
        else:
            return None

    # Gets all items in players inventory, gets the names of those items and forms them into a string to return
    def get_all_items_in_room(self, room_id):
        self.cursor.execute('SELECT room_items FROM dungeon WHERE room_id = ?',
                            (room_id,))
        result = self.cursor.fetchone()  # retrieve the first row
        # check result is not none
        if result[0] != None:
            all_items = ''
            # Split the string of items into a list
            split_input = result[0].split(',')
            # For every item get its name and add to a message to return
            for item in split_input:
                if item != '' or item != ' ':
                    item_name = self.get_item_name(item)
                    if item_name is not None:
                        all_items += item_name + ' '
            if all_items == '':
                return None
            else:
                return all_items
        else:
            return None

    # Gets all items in the players inventory, gets the names of those items and forms them into a string to return
    def get_all_items_in_inventory(self, my_player):
        self.cursor.execute('SELECT player_inventory FROM players WHERE player_name = ?',
                            (my_player,))
        result = self.cursor.fetchone()  # retrieve the first row
        # check result is not none
        if result[0] != None:
            all_items = ''
            # Split the string of items into a list
            split_input = result[0].split(',')
            # For every item get its name and add to a message to return
            for item in split_input:
                item_name = self.get_item_name(item)
                if item_name != None:
                    all_items += item_name + ' '
            if all_items == '':
                return None
            else:
                return all_items
        else:
            return None

    def pickup_item(self, item_name, my_player, room_id):
        # Get item id
        item_id = self.get_item_id(item_name)
        if item_id is not None:
            # Check room location for item
            result = self.get_all_items_in_room(room_id)
            if result is not None:
                split_input = result.split(' ')
                for item in split_input:
                    # If the item is in the room give it to the player
                    if item == item_name:
                        self.give_item(item_id, my_player=my_player, to_player=True)
                        # remove item from room
                        self.remove_item(item_id, room_id=room_id, from_room=True)
                        # return item moved
                        return 'You have picked up ' + item_name
                return 'No item by that name in this room'
            return 'No item by that name in this room'
        # if no return no item in location
        else:
            return 'No item by that name in this room'

    def drop_item(self, item_name, my_player, room_id):
        # Get item id
        item_id = self.get_item_id(item_name)
        if item_id is not None:
            # Check room location for item
            result = self.get_all_items_in_inventory(my_player)
            if result is not None:
                split_input = result.split(' ')
                for item in split_input:
                    # If the item is in the room give it to the player
                    if item == item_name:
                        self.give_item(item_id, room_id=room_id, to_room=True)
                        # remove item from room
                        self.remove_item(item_id, my_player=my_player, from_player=True)
                        # return item moved
                        return 'You have dropped ' + item_name
                return 'No item by that name in your inventory'
            return 'No item by that name in your inventory'
        # if no return no item in location
        else:
            return 'No item by that name in your inventory'

    # Give item to player
    def give_item(self, item_id, room_id=0, my_player='', to_player=False, to_room=False):
        if to_player:
            result = self.get_all_items_in_inventory(my_player)
        elif to_room:
            result = self.get_all_items_in_room(room_id)
        all_items = ''
        if result != None:
            split_input = result.split(' ')
            for item in split_input:
                current_item_id = self.get_item_id(item)
                if current_item_id is not None:
                    all_items += str(current_item_id) + ','
        if item_id is not None:
            all_items += str(item_id) + ','
        if to_player:
            self.cursor.execute('UPDATE players SET player_inventory = ? WHERE player_name = ?',
                                (all_items, my_player,))
        elif to_room:
            self.cursor.execute('UPDATE dungeon SET room_items = ? WHERE room_id = ?',
                                (all_items, room_id,))
        self.db.commit()

    # Removes an item from a room
    def remove_item(self, item_id, room_id=0, my_player='', from_player=False, from_room=False):
        if from_room:
            result = self.get_all_items_in_room(room_id)
        elif from_player:
            result = self.get_all_items_in_inventory(my_player)
        split_input = result.split(' ')
        all_items = ''
        removed = False
        for item in split_input:
            current_item_id = self.get_item_id(item)
            # If the item matches but hasn't been removed yet, skip it and set removed to true
            if current_item_id == item_id and removed is False:
                removed = True
            # If the item matches but one has already been removed add it back to the list
            elif current_item_id == item_id and removed is True:
                all_items += str(current_item_id) + ','
            # all items that don't match go back in the list
            elif current_item_id != item_id and current_item_id is not None:
                all_items += str(current_item_id) + ','
        # Set new items in db and update
        if from_room:
            self.cursor.execute('UPDATE dungeon SET room_items = ? WHERE room_id = ?',
                                (all_items, room_id,))
        elif from_player:
            self.cursor.execute('UPDATE players SET player_inventory = ? WHERE player_name = ?',
                                (all_items, my_player,))
        self.db.commit()

    # Sets the players current room
    def set_current_room(self, my_player, new_room):
        self.cursor.execute('UPDATE players SET current_room = ? WHERE player_name = ?',
                            (new_room, my_player,))
        self.db.commit()
        print('Updated current room')

    # Update a value
    def change_value(self, table_name, field_to_change, new_value, query_field, query_value):
        # Insert user
        self.cursor.execute('UPDATE ' + table_name + ' SET ' + field_to_change + ' = ? WHERE ' + query_field + ' = ?',
                            (new_value, query_value,))
        self.db.commit()
        print(field_to_change + ' updated')

    # Create table to store all users
    def create_user_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users(
                        username TEXT PRIMARY KEY, 
                        password TEXT, 
                        salt TEXT)
                        ''')
        # commit the change
        self.db.commit()
        print('User table created')

    # Create table to store all players
    def create_player_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS players(
                        id INTEGER PRIMARY KEY, 
                        owner_username TEXT, 
                        current_room INTEGER DEFAULT 1, 
                        player_name TEXT,
                        player_inventory TEXT,
                        player_equipment TEXT)
                        ''')
        # commit the change
        self.db.commit()
        print('Player table created')

    # Create table to store all players
    def create_dungeon_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS dungeon(
                        room_id INTEGER PRIMARY KEY, 
                        room_name TEXT,
                        base_description TEXT, 
                        detailed_description TEXT, 
                        north INTEGER DEFAULT '', 
                        east INTEGER DEFAULT '', 
                        south INTEGER DEFAULT '', 
                        west INTEGER DEFAULT '',
                        room_items TEXT)
                        ''')
        # commit the change
        self.db.commit()
        print('Dungeon table created')

    # Create table to store all items
    def create_item_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS items(
                        item_id INTEGER PRIMARY KEY, 
                        item_name TEXT,
                        item_weight TEXT,
                        item_body_part TEXT,
                        item_damage TEXT,
                        item_defence)
                        ''')
        # commit the change
        self.db.commit()
        print('Item table created')
