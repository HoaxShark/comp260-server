from Scripts import input
from Scripts import window

from PyQt5.QtWidgets import QApplication
from time import sleep

import sys
import threading
import socket

class Client:

    def __init__(self):
        self.is_connected = False
        self.my_socket = None
        self.is_running = True
        self.app = QApplication(sys.argv)
        self.my_window = window.Window()
        self.input_manager = ''

    def receive_thread(self):
        while self.is_running:
            if self.is_connected:
                try:
                    self.my_window.messageQueue.put(self.my_socket.recv(4096).decode("utf-8"))
                    print("Adding to queue")
                except socket.error:
                    self.my_socket = None
                    self.is_connected = False
                    print("Server lost.")
                    sleep(2)

    def connection_thread(self, input_manager):
        while self.is_running:
            # if not connected loop here trying to connect until success
            while self.is_connected == False:
                if self.my_socket == None:
                    # create a socket
                    self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    # connect to the IP address using port
                    self.my_socket.connect(("127.0.0.1", 8222))
                    self.is_connected = True
                    # update the socket in the input_manager
                    self.input_manager.my_socket = self.my_socket
                    print("Connected to Server.")
                    sleep(2)

                except socket.error:
                    self.is_connected = False
                    print("no luck connecting, try again in 2 secs")
                    sleep(2)

    # Entry point of programme
    def main(self):
        # create input manager used to lower input and send to server.
        self.input_manager = input.Input(self.my_socket)
        # pass input_manager to the window
        self.my_window.input_manager = self.input_manager
        # start connection thread which deals with general updates, sending to server
        my_connection_thread = threading.Thread(target=self.connection_thread, args=(self.input_manager,))
        my_connection_thread.start()
        # start the receive thread running
        my_receive_thread = threading.Thread(target=self.receive_thread)
        my_receive_thread.start()

        while self.is_running:
            # draw the gui window
            self.my_window.window_draw()
            # exit the gui window
            sys.exit(self.app.exec_())

        print('Exiting Dungeon')
        self.my_socket.close()


# If this is __main__ then run entry point
if __name__ == '__main__':
    client = Client()
    client.main()

