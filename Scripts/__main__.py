from Scripts import player


# Entry point of programme
def main():
    player_ref = player.Player(1)
    player_ref.player_input()
    print('Exiting Dungeon')


# If this is __main__ then run entry point
if __name__ == '__main__':
    main()