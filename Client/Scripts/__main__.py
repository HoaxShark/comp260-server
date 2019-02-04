from Scripts import input
from time import sleep

import threading
import socket


# Entry point of programme
def main():
    # create a socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the IP address using port
    my_socket.connect(("127.0.0.1", 8222))
    connected = True
    print("Connected to Server.")

    input_manager = input.Input(my_socket)

    #threading_1 = threading.Thread(target=input_manager.player_input(my_socket))
    #threading_1.daemon = True
    #threading_1.start()
#
    #threading_2 = threading.Thread(target=receive_data(my_socket))
    #threading_2.daemon = True
    #threading_2.start()

    while True:
        # send user input to the server then wait for data back
        try:
            input_manager.player_input(my_socket)
            receive_data(my_socket)

        except socket.error:
            print("Server Lost. Will try and reconnect.")
            connected = False
            while not connected:
                # try to reconnect, else sleep 2 seconds try again
                try:
                    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    my_socket.connect(("127.0.0.1", 8222))
                    connected = True
                    print("Re-connection successful")
                except socket.error:
                    print("no luck connecting, try again in 2 secs")
                    sleep(2)

    print('Exiting Dungeon')
    my_socket.close()


def receive_data(my_socket):
    data = my_socket.recv(4096)
    print(data.decode("utf-8"))


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
