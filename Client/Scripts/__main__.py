from Scripts import player
from Scripts import dungeon
import socket
#from Scripts import window
import sys
#from PyQt5 import QtGui


# Entry point of programme
def main():
    # create a socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the IP address using port
    my_socket.connect(("127.0.0.1", 8222))

    dungeon_ref = dungeon.Dungeon()
    player_ref = player.Player(dungeon_ref, 'Hall')
    print(player_ref.game_running)

    while player_ref.game_running:
        data = my_socket.recv(4096)
        print(data.decode("utf-8"))
        player_ref.player_input()
        my_socket.send(player_ref.lowered_input.encode())
        #dungeon_ref.update_dungeon()

    print('Exiting Dungeon')


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()
