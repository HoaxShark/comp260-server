from Scripts import player
from Scripts import dungeon
from Scripts import window
import sys
from PyQt5 import QtGui


# Entry point of programme
def main():
    dungeon_ref = dungeon.Dungeon()
    player_ref = player.Player(dungeon_ref, 'Hall')
    print(player_ref.game_running)

    #gui = window.Window()
    #app_ref = QtGui.QApplication(sys.argv)


    while player_ref.game_running:
        #gui.window_draw()
        player_ref.player_input()
        dungeon_ref.update_dungeon()


    print('Exiting Dungeon')


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()