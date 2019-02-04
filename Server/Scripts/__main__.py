import socket

from Scripts import input
from Scripts import player
from Scripts import dungeon

if __name__ == '__main__':

    # create the socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setup the socket ip address
    my_socket.bind(("127.0.0.1", 8222))
    # listen for new connections / waits here until a client connects
    my_socket.listen(5)
    # new client has connected
    client = my_socket.accept()

    # generate dungeon
    my_dungeon = dungeon.Dungeon()
    my_player = player.Player(my_dungeon, 'Hall')
    input_manager = input.Input()

    while True:
        try:
            # receive data from client
            data = client[0].recv(4096)
            # print received data
            print("Input from client: " + data.decode("utf-8"))
            # send input from client to the input manager
            client_reply = input_manager.player_input(data.decode("utf-8"), my_player, my_dungeon)
            # send back the data received
            client[0].send(client_reply.encode())

        except socket.error:
            print("Client Lost")
            # listen for new connections / waits here until a client connects
            my_socket.listen(5)
            # new client has connected
            client = my_socket.accept()
