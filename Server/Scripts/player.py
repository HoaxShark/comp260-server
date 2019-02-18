class Player:

    def __init__(self, dungeon, start_room):
        self.current_room: str = start_room  # Room the player is currently in
        self.dungeon_ref = dungeon  # The entire dungeon
        self.player_id: int = 0  # Identification tag of the player
        self.current_weight: int = 0  # The current weight of everything the player has
        self.max_weight: int  # Maximum weight the player can reach before being unable to move
        self.inventory = {}  # Items the player has on them
        self.equipped = {}  # Items the player had equipped
        self.player_name = 'Ryan'  # name of player
