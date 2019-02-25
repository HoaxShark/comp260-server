import socket
import threading
import time
from queue import *

from Scripts import input
from Scripts import player
from Scripts import dungeon

# dictionary of all connected clients
clients = {}
# lock for protecting the client dictionary
clientsLock = threading.Lock()

# queue of all messages received
message_queue = Queue()

lost_clients = []


# used as a thread. created for each connected client, receives their input and stores in a queue
# with the client socket and the message
def receive_thread(client_socket):
    receive_is_running = True
    while receive_is_running:
        try:
            # store the client and message in the queue
            message_queue.put((client_socket, client_socket.recv(4096).decode("utf-8")))
            print("Adding to queue")
        except socket.error:
            print("Client lost.")
            lost_clients.append(client_socket)
            receive_is_running = False


# used in a thread. looks for new clients and adds them to the dictionary when they connect
def accept_clients(server_socket):
    while is_running:
        print("Looking for new clients.")
        # client has been found
        new_client = server_socket.accept()
        print("Added client. Socket info: " + str(new_client[0]))
        # lock the clients dictionary
        clientsLock.acquire()
        # store the new client in the dictionary and apply a new player to it
        clients[new_client[0]] = player.Player(my_dungeon, '1')
        print(clients.get(new_client[0]))
        # create a receive message thread for the client
        my_receive_thread = threading.Thread(target=receive_thread, args=(new_client[0],))
        my_receive_thread.start()

        start_message = 'You stand in the city of Elerand, before you stands the magnficent church of Phelonia, known to have trained the greatest of holy knights.\n'
        new_client[0].send(start_message.encode())

        # update the client list in input_manager
        input_manager.all_connected_clients = clients
        # release the lock on the dictionary
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
    input_manager = input.Input()

    # start the thread that accepts new clients
    my_accept_thread = threading.Thread(target=accept_clients, args=(my_socket, ))
    my_accept_thread.start()

    while is_running:
        client_and_message = ''

        clientsLock.acquire()
        while message_queue.qsize() > 0:
            try:
                client_and_message = message_queue.get()
                # print received data
                # print("Input from client " + str(client_and_message[0]) + ": \n" + client_and_message[1])
                # send input from client to the input manager
                client_reply = input_manager.player_input(client_and_message[1], client_and_message[0], my_dungeon)
                if client_reply is not None:
                    # send back the data received
                    client_and_message[0].send(client_reply.encode())

            except socket.error:
                # add the lost client to the list of lost clients
                lost_clients.append(client_and_message[0])
                print("Client Lost")

        for client in lost_clients:
            # pop the lost client from the dictionary of clients
            clients.pop(client)
            # update the client list in input_manager
            input_manager.all_connected_clients = clients

        # clear list of lost clients
        lost_clients = []

        clientsLock.release()

        time.sleep(0.5)


