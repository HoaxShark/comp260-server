from Scripts import input
import socket


# Entry point of programme
def main():
    # create a socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the IP address using port
    my_socket.connect(("127.0.0.1", 8222))

    input_manager = input.Input()

    while True:

        input_manager.player_input()
        my_socket.send(input_manager.lowered_input.encode())
        data = my_socket.recv(4096)
        print(data.decode("utf-8"))

    print('Exiting Dungeon')


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
