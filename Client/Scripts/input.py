import bcrypt
import json


class Input:

    def __init__(self, my_socket):
        self.my_socket = my_socket
        # Salt to be used with the passwords
        self.salt = ''
        # Users login password
        self.password = ''
        # Users login username
        self.username = ''
        # Used to confirm to the server that the incoming packets should be read
        self.packet_ID = 'BestMUD'
        # Stores the encryption key from the server
        self.encryption_key = ''

    def set_salt(self, salt):
        self.salt = salt

    def set_username_password(self, username, password):
        self.username = username
        self.password = password

    def send_username(self):
        message = '#username ' + self.username
        self.send_message(message)

    def send_password(self):
        # Encode password and salt
        self.password = self.password.encode('utf-8')
        self.salt = self.salt.encode('utf-8')
        # Hash password
        self.password = bcrypt.hashpw(self.password, self.salt)
        # Decode password
        self.password = self.password.decode()
        message = '#username_salt ' + self.password
        self.send_message(message)

    def send_message(self, message):
        # Dictionary of information to send to the server, room to expand
        my_dict = {'message': message}
        # Transform dictionary into json
        json_packet = json.dumps(my_dict)
        # Header used to inform the server of the upcoming packet size
        header = len(json_packet).to_bytes(2, byteorder='little')

        if self.my_socket is not None:
            # Send all required information to the server
            self.my_socket.send(self.packet_ID.encode())
            self.my_socket.send(header)
            self.my_socket.send(json_packet.encode())
