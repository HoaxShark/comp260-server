from Scripts import input
from time import sleep

import threading
import socket


# Entry point of programme
def main():

    is_connected = False
    my_socket = None
    is_running = True

    input_manager = input.Input(my_socket)

    #threading_1 = threading.Thread(target=input_manager.player_input(my_socket))
    #threading_1.daemon = True
    #threading_1.start()
#
    #threading_2 = threading.Thread(target=receive_data(my_socket))
    #threading_2.daemon = True
    #threading_2.start()

    while is_running:
        # if not connected loop here trying to connect until success
        while not is_connected:
            if my_socket == None:
                # create a socket
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                receive_data(my_socket)

            except socket.error:
                print("Server Lost. Will try and reconnect.")
                my_socket = None
                is_connected = False

    print('Exiting Dungeon')
    my_socket.close()


def receive_data(my_socket):
    data = my_socket.recv(4096)
    print(data.decode("utf-8"))


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
