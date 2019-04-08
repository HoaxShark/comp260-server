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
        self.cursor.execute('''SELECT ? FROM {} WHERE ? = ?'''.format(table_name), (field_to_check, query_field, query_value,))
        result = self.cursor.fetchone()  # retrieve the first row
        return result

    # Checks the db for a matching value returns 0 if it doesn't match and 1 if it does
    def check_value(self, table_name, field_to_check, value_to_check, query_field, query_value):
        self.cursor.execute('''SELECT ? FROM ? WHERE ? = ?''', (field_to_check, table_name, query_field, query_value,))
        result = self.cursor.fetchone()  # retrieve the first row
        if result == value_to_check:
            return 1
        elif result != value_to_check:
            return 0

    # Update a value
    def change_value(self, table_name, field_to_change, new_value, query_field, query_value):
        # Insert user
        self.cursor.execute('''UPDATE ? SET ? = ? WHERE ? = ? ''', (table_name, field_to_change, new_value, query_field, query_value,))
        self.db.commit()
        print(field_to_change + ' updated')

    # Create table to store all users
    def create_user_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY, 
                        username TEXT, 
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
                        id INTEGER PRIMARY KEY, 
                        room_id INTEGER, 
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
