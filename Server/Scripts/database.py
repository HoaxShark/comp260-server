import sqlite3


class Database:

    def __init__(self):
        # create or open a file called my_db
        self.db = sqlite3.connect('server_db')
        # get cursor object
        self.cursor = self.db.cursor()

    def create_user_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)
                        ''')
        # commit the change
        self.db.commit()
        print('User table created')

    # Adds a new user to the db
    def add_user(self, name, password, salt):
        # Insert user
        self.cursor.execute('''INSERT INTO users(username, password, salt)
                          VALUES(?,?,?)''', (name, password, salt))
        self.db.commit()
        print('User inserted')

    # Returns the salt for the password encryption
    def get_salt(self, name):
        self.cursor.execute('''SELECT salt FROM users WHERE username=?''', (name,))
        salt = self.cursor.fetchone()  # retrieve the first row
        return salt

    # Checks the db for a matching username returns 0 if it doesn't exist and 1 if it does
    def check_name(self, name):
        self.cursor.execute('''SELECT username FROM users WHERE username=?''', (name,))
        user = self.cursor.fetchone()  # retrieve the first row
        if user is None:
            return 0
        elif user is not None:
            return 1

    # Checks the db for a matching password returns 0 if it doesn't match and 1 if it does
    def check_password(self, name, password):
        self.cursor.execute('''SELECT password FROM users WHERE username=?''', (name,))
        db_password = self.cursor.fetchone()  # retrieve the first row
        if db_password == password:
            return 1
        elif db_password != password:
            return 0

    # Update the users password
    def change_password(self, name, password):
        # Insert user
        self.cursor.execute('''UPDATE users SET password =? WHERE name = ? ''', (password, name))
        self.db.commit()
        print('Password updated')

    # Create table to store all players
    def create_player_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS players(id INTEGER PRIMARY KEY, current_room TEXT, max_weight TEXT, inventory TEXT, equipped TEXT, player_name TEXT)
                        ''')
        # commit the change
        self.db.commit()
        print('Player table created')

    # CARRY ON WITH THIS
    def get_player_data(self, name):
        self.cursor.execute('''SELECT * FROM players WHERE player_name=?''', (name,))
        salt = self.cursor.fetchone()  # retrieve the first row
        return salt