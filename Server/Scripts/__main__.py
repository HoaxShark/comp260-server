import socket
import threading
import time

from Scripts import input
from Scripts import player
from Scripts import dungeon

# dictionary of all connected clients
clients = {}
# lock for protecting the client dictionary
clientsLock = threading.Lock()


# used in a thread. looks for new clients and adds them to the dictionary when they connect
def accept_clients(server_socket):
    while is_running:
        print("Looking for new clients.")
        new_client = server_socket.accept()
        print("Added client. Socket info: " + str(new_client[0]))
        clientsLock.acquire()
        clients[new_client[0]] = 0
        clientsLock.release()
        # is_connected = True


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

    my_accept_thread = threading.Thread(target=accept_clients, args=(my_socket, ))
    my_accept_thread.start()

    while is_running:
        lost_clients = []

        clientsLock.acquire()
        for client in clients:
            try:
                # receive data from client
                data = client.recv(4096)
                # print received data
                print("Input from client " + str(client) + ": " + data.decode("utf-8"))
                # send input from client to the input manager
                client_reply = input_manager.player_input(data.decode("utf-8"), my_player, my_dungeon)
                # send back the data received
                client.send(client_reply.encode())

            except socket.error:
                lost_clients.append(client)
                print("Client Lost")

        for client in lost_clients:
            clients.pop(client)

        clientsLock.release()

        time.sleep(0.5)


