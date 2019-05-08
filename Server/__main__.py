import socket
import threading
import time
import json

from base64 import b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

from queue import *
from Scripts import input
from Scripts import database

# Generate the encryption key for this instance
encryption_key = get_random_bytes(16)

# dictionary of all connected clients
clients = {}
# lock for protecting the client dictionary
clientsLock = threading.Lock()

# queue of all messages received
message_queue = Queue()

lost_clients = []

# True if testing on a local host
local_host = True

db = database.Database()


# used as a thread. created for each connected client, receives their input and stores in a queue
# with the client socket and the message
def receive_thread(client_socket):
    receive_is_running = True
    while receive_is_running:
        try:
            # Get the ID packet
            packet_id = client_socket.recv(7)

            if packet_id.decode('utf-8') == 'BestMUD':
                # Get size of incoming data
                payload_size = int.from_bytes(client_socket.recv(2), 'little')
                payload_data = client_socket.recv(payload_size)
                payload_data = payload_data.decode('utf-8')
                # Get payload data is a dict format
                data_from_client = json.loads(payload_data)
                # Decrypt data
                iv = b64decode(data_from_client['iv'])
                ciphertext = b64decode(data_from_client['ciphertext'])
                cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
                decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)

                # Store message from client in the queue
                message_queue.put((client_socket, decrypted_message.decode('utf-8')))

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
        clients[new_client[0]] = 0  # player.Player(my_dungeon, '1')
        print(clients.get(new_client[0]))
        # create a receive message thread for the client
        my_receive_thread = threading.Thread(target=receive_thread, args=(new_client[0],))
        my_receive_thread.start()

        #start_message = 'You stand in the city of Elerand, before you stands the magnficent church of Phelonia, known to have trained the greatest of holy knights.\n'

        # Send setup message to the client with encryption key information
        input_manager.send_setup_info(encryption_key, new_client[0])
        # Add the client into the input_manager client list
        input_manager.all_connected_clients[new_client[0]] = 0
        # add new client to the login area
        input_manager.add_client_to_login_area(new_client[0])
        # release the lock on the dictionary
        clientsLock.release()


if __name__ == '__main__':

    is_running = True
    is_connected = False

    # create the socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if local_host:
        # setup the socket ip address for local testing
        my_socket.bind(("127.0.0.1", 8222))
    else:
        # setup the socket ip address for server testing
        my_socket.bind(("46.101.56.200", 9199))
    # listen for new connections / waits here until a client connects
    my_socket.listen(5)

    # generate input manager
    input_manager = input.Input()

    # Set the encryption key in the input manager
    input_manager.encryption_key = encryption_key

    # start the thread that accepts new clients
    my_accept_thread = threading.Thread(target=accept_clients, args=(my_socket, ))
    my_accept_thread.start()

    while is_running:
        client_and_message = ''

        clientsLock.acquire()
        while message_queue.qsize() > 0:
            try:
                client_and_message = message_queue.get()
                # send input from client to the input manager
                client_reply = input_manager.player_input(client_and_message[1], client_and_message[0])
                if client_reply is not None:
                    # send back the data received
                    input_manager.send_message(client_reply, client_and_message[0])

            except socket.error:
                # add the lost client to the list of lost clients
                lost_clients.append(client_and_message[0])
                print("Client Lost")

        for client in lost_clients:
            # pop the lost client from the dictionary of clients
            clients.pop(client)
            # Clear client from lists in input manager
            input_manager.clear_client_from_lists(client)
            # update the client list in input_manager
            input_manager.all_connected_clients = clients

        # clear list of lost clients
        lost_clients = []

        clientsLock.release()

        time.sleep(0.5)


