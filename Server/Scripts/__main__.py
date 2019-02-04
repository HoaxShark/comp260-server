import socket

from Scripts import input
from Scripts import player
from Scripts import dungeon

if __name__ == '__main__':

    # create the socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setup the socket ip address
    mySocket.bind(("127.0.0.1", 8222))
    # listen for new connections / waits here until a client connects
    mySocket.listen(5)
    # new client has connected
    client = mySocket.accept()

    # generate dungeon
    my_dungeon = dungeon.Dungeon()
    my_player = player.Player(my_dungeon, 'Hall')
    input_manager = input.Input()

    while True:
        # receive data from client
        data = client[0].recv(4096)
        # print received data
        print("Input from client: " + data.decode("utf-8"))
        # send input from client to the input manager
        client_reply = input_manager.player_input(data.decode("utf-8"), my_player, my_dungeon)
        # send back the data received
        client[0].send(client_reply.encode())
