from Scripts import input
import socket


# Entry point of programme
def main():
    my_socket = socket_create_connect()

    input_manager = input.Input(my_socket)

    while True:
        input_manager.player_input()
        # if player tries to reconnect to the server
        #if input_manager.lowered_input == 'connect':
        #    my_socket.close()
        #    socket_create_connect()

        try:
            my_socket.send(input_manager.lowered_input.encode())
            data = my_socket.recv(4096)
            print(data.decode("utf-8"))
        except socket.error:
            print("Server Lost. Type 'connect' to try and reconnect.")

    print('Exiting Dungeon')


def socket_create_connect():
    # create a socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the IP address using port
    my_socket.connect(("127.0.0.1", 8222))

    return my_socket

# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
