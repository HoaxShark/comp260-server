class Item:

    def __init__(self, name, weight, max_durability):
        self.name = name
        self.weight = weight
        self.max_durability = max_durability
        self.durability = max_durability


class Weapon(Item):

    def __init__(self, name, weight, max_durability, damage, body_part):
        super().__init__(name, weight, max_durability)
        self.damage = damage
        self.body_part = body_part


class Armour(Item):

    def __init__(self, name, weight, max_durability, defence, body_part):
        super().__init__(name, weight, max_durability)
        self.defence = defence
        self.body_part = body_part
