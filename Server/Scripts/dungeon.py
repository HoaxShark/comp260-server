from Scripts import timer


class Room:

    def __init__(self, name, description, look_description, north='', east='', south='', west=''):
        self.name = name
        self.description = description
        self.look_description = look_description
        self.north_connection = north
        self.east_connection = east
        self.south_connection = south
        self.west_connection = west


class Dungeon:

    rooms: Room = {}
    time: int

    def __init__(self):
        self.populate_dungeon()
        self.timer_ref = timer.Timer()
        self.players = {}  # dictionary of all players in the dungeon

    def update_dungeon(self):
        self.timer_ref.update_time()
        print(self.timer_ref.minute)

    def populate_dungeon(self):
        self.rooms['Hall'] = Room('Hall', 'A grand hallway with a door leading east', 'The ceiling in the hallway '
                                  'looks as though it extends into the heavens, the large wooden door to the east '
                                  'has a unnerving aura about it.', east='Outside')
        self.rooms['Outside'] = Room('Outside', 'The outside, better go back in to the west', 'Unknown sounds shock '
                                     'your ears, the brightness closed your eyes, but now you strain to open them. '
                                     'The light burns and constantly berates your eyes.', west='Hall')
