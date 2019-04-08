from Scripts import timer
from Scripts import item


class Room:

    def __init__(self, room_id, name, description, look_description, north='', east='', south='', west='', items={}):
        self.id = room_id
        self.name = name
        self.description = description
        self.look_description = look_description
        self.north_connection = north
        self.east_connection = east
        self.south_connection = south
        self.west_connection = west
        self.items = items


class Dungeon:

    def __init__(self):
        self.rooms = {}
        self.populate_dungeon()
        self.timer_ref = timer.Timer()
        self.players = {}  # dictionary of all players in the dungeon
        self.time = 0

    def update_dungeon(self):
        self.timer_ref.update_time()
        print(self.timer_ref.minute)

    def populate_dungeon(self):
        self.rooms['1'] = Room('1', 'Outside Church',
                               'To the north a large church towers over you.\n',
                               'The church glows, adorned in marble and gold, the large wooden doors to the north have a smaller'
                               ' door built into them, it gives off a welcoming feeling.\n',
                               north='100')
        self.rooms['100'] = Room('100', 'Church Entrance',
                                 'Holy statues stand throughout the hall pointing north to the center of the church. The main enterance lies to the south.\n',
                                 'You recognise the statues of deities, Azur and Benath two of the holy knights of legend.\n',
                                 south='1',
                                 north='101',
                                 items={item.Weapon("Sword of Benath", 10, 100, 5, "right_hand"):'Sword of Benath', item.Weapon("Candle", 10, 100, 20, "right_hand"):'Candle' })
        self.rooms['101'] = Room('101', 'Church Center',
                                 'You stand in the center of the church, enterances to both wings sit on the east and west, to the north lies the main alter and south is the enterance hall.\n',
                                 'On deeper inspection you see that the two wings have been locked down and the altar is being blocked by a hudle people.\n',
                                 south='100',
                                 items={item.Armour("Chestplate", 50, 100, 20, "chest"):'Chestplate',
                                        item.Armour("Hat", 5, 100, 2, "head"):'Hat',item.Armour("Gloves", 4, 100, 2, "hands"):'Gloves',
                                        item.Armour("Gauntlets", 30, 100, 10, "hands"):'Gauntlets',item.Armour("Trousers", 15, 100, 7, "legs"):'Trousers',
                                        item.Armour("Boots", 10, 100, 5, "feet"):'Boots'})
