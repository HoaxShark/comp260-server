from Scripts import input
from Scripts import window

from PyQt5.QtWidgets import QApplication
from time import sleep
from queue import *

import sys
import threading
import socket

# queue that holds all messages from the server
messageQueue = Queue()
is_connected = False
my_socket = None
is_running = True
app = QApplication(sys.argv)
my_window = window.Window()


def receive_thread(server_socket):
    global is_connected
    global is_running
    global my_socket

    while is_running:
        if is_connected:
            try:
                messageQueue.put(server_socket.recv(4096).decode("utf-8"))
                print("Adding to queue")
            except socket.error:
                my_socket = None
                is_connected = False
                print("Server lost.")


# Entry point of programme
def main():
    global is_connected
    global my_socket
    global is_running

    input_manager = input.Input(my_socket)

    while is_running:
        # draw the gui window
        my_window.window_draw()
        # exit the gui window
        sys.exit(app.exec_())

        # if not connected loop here trying to connect until success
        while not is_connected:
            if my_socket == None:
                # create a socket
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                my_receive_thread = threading.Thread(target=receive_thread, args=(my_socket,))
                my_receive_thread.start()

            try:
                # connect to the IP address using port
                my_socket.connect(("127.0.0.1", 8222))
                is_connected = True
                print("Connected to Server.")

            except socket.error:
                is_connected = False
                print("no luck connecting, try again in 2 secs")
                sleep(2)

        # main play loop sends and receives data to server
        while is_connected:
            try:
                input_manager.player_input(my_socket)
                sleep(0.5)

            except socket.error:
                print("Server Lost. Will try and reconnect.")
                my_socket = None
                is_connected = False

            while messageQueue.qsize() > 0:
                print(messageQueue.get())

    print('Exiting Dungeon')
    my_socket.close()


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
