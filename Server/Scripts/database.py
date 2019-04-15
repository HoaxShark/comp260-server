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
        return result[0]

    # Gets the players current room
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
                        player_name TEXT)
                        ''')
        # commit the change
        self.db.commit()
        print('Player table created')

    # Create table to store all players
    def create_dungeon_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS dungeon(
                        room_id INTEGER PRIMARY KEY, 
                        base_description TEXT, 
                        detailed_description TEXT, 
                        north INTEGER DEFAULT '', 
                        east INTEGER DEFAULT '', 
                        south INTEGER DEFAULT '', 
                        west INTEGER DEFAULT '')
                        ''')
        # commit the change
        self.db.commit()
        print('Dungeon table created')
