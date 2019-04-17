from Scripts import input
from Scripts import window

from PyQt5.QtWidgets import QApplication
from time import sleep

import sys
import threading
import socket
import json

local_host = True


class Client:

    def __init__(self):
        self.is_connected = False
        self.my_socket = None
        self.is_running = True
        self.app = QApplication(sys.argv)
        self.my_window = window.Window()
        self.input_manager = ''
        self.client = ''
        self.my_connection_thread = ''
        self.my_receive_thread = ''

    def set_client(self, this_client):
        self.client = this_client
        self.my_window.set_client(self.client)

    def receive_thread(self):
        while self.is_running:
            if self.is_connected:
                try:
                    # Get the ID packet
                    packet_id = self.my_socket.recv(7)

                    if packet_id.decode('utf-8') == 'BestMUD':
                        # Get size of incoming data
                        payload_size = int.from_bytes(self.my_socket.recv(2), 'little')
                        payload_data = self.my_socket.recv(payload_size)
                        # Get payload data is a dict format
                        data_from_server = json.loads(payload_data)
                        # Store message from client in the queue
                        self.my_window.message_queue.put(data_from_server['message'])

                except socket.error:
                    self.my_socket = None
                    self.is_connected = False
                    self.my_window.textEdit.append("<font color='red'>Server lost.</font>")
                    sleep(2)

    def connection_thread(self):
        while self.is_running:
            # if not connected loop here trying to connect until success
            while self.is_connected is False:
                if self.my_socket is None:
                    # create a socket
                    self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    if local_host:
                        # connect to the IP address using port for local hosting
                        self.my_socket.connect(("127.0.0.1", 8222))
                    else:
                        # connect to the IP address using port for server hosting
                        self.my_socket.connect(("46.101.56.200", 9199))
                    self.is_connected = True
                    # update the socket in the input_manager
                    self.input_manager.my_socket = self.my_socket
                    self.my_window.textEdit.append("<font color='green'>Connected to server.</font>")
                    # When connected set connected to True for the window
                    self.my_window.set_connected(True)
                    sleep(2)

                except socket.error:
                    self.my_window.set_connected(False)
                    self.is_connected = False
                    # No connection so reset logged in
                    self.my_window.set_logged_in(False)
                    self.my_window.textEdit.append("<font color='red'>Connection attempt failed. Trying again.</font>")
                    sleep(2)

    # Entry point of programme
    def main(self):
        # create input manager used to lower input and send to server.
        self.input_manager = input.Input(self.my_socket)
        # pass input_manager to the window
        self.my_window.input_manager = self.input_manager
        # start connection thread which deals with general updates, sending to server
        self.my_connection_thread = threading.Thread(target=self.connection_thread)
        self.my_connection_thread.start()
        # start the receive thread running
        self.my_receive_thread = threading.Thread(target=self.receive_thread)
        self.my_receive_thread.start()

        # draw the gui window
        self.my_window.window_draw()
        # exit the gui window
        sys.exit(self.app.exec_())


# If this is __main__ then run entry point
if __name__ == '__main__':
    client = Client()
    client.set_client(client)
    client.main()

