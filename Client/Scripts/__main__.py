from Scripts import input
from time import sleep

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

    while True:
        # handle player input
        input_manager.player_input()

        # if player tries to reconnect to the server
        if input_manager.lowered_input == 'connect':
            my_socket.connect(("127.0.0.1", 8222))

        # send user input to the server then wait for data back
        try:
            my_socket.send(input_manager.lowered_input.encode())
            data = my_socket.recv(4096)
            print(data.decode("utf-8"))
        except socket.error:
            print("Server Lost. Type 'connect' to try and reconnect.")
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


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
