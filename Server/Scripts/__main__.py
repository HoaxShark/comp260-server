import socket
import threading

from Scripts import input
from Scripts import player
from Scripts import dungeon

# dictionary of all connected clients
clients = {}
# lock for protecting the client dictionary
clientsLock = threading.Lock()

if __name__ == '__main__':

    is_running = True
    is_connected = False

    # create the socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setup the socket ip address
    my_socket.bind(("127.0.0.1", 8222))
    # listen for new connections / waits here until a client connects
    my_socket.listen(5)

    # generate dungeon
    my_dungeon = dungeon.Dungeon()
    my_player = player.Player(my_dungeon, 'Hall')
    input_manager = input.Input()

    while is_running:
        while not is_connected:
            print("Waiting for client.")
            # new client has connected
            client = my_socket.accept()
            print("Client connected.")
            is_connected = True
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
            is_connected = False

def accept_client(server_socket):
    # do server connections here