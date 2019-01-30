from Scripts import player
from Scripts import dungeon


# Entry point of programme
def main():
    dungeon_ref = dungeon.Dungeon()
    player_ref = player.Player(dungeon_ref, 'Hall')

    while player_ref.game_running:
        player_ref.player_input()

    print('Exiting Dungeon')


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()