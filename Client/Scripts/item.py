class Item:

    name = ''
    weight = ''
    durability = ''
    max_durability = ''

    def __init__(self, name, weight, max_durability):
        self.name = name
        self.weight = weight
        self.max_durability = max_durability
        self.durability = max_durability


class Weapon(Item):

    damage = ''

    def __init__(self, name, weight, max_durability, damage):
        super().__init__(name, weight, max_durability)
        self.damage = damage


class Armour(Item):

    defence = ''
    body_part = ''

    def __init__(self, name, weight, max_durability, defence, body_part):
        super().__init__(name, weight, max_durability)
        self.defence = defence
        self.body_part = body_part
