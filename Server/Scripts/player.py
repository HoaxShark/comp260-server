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

    def equip_item(self, item_name):
        # for every item in the players inventory
        for item in self.inventory:
            # check if the item matches the requested one
            if item_name == item.name.lower():
                # check that an item isn't already equipped to the body part
                for equipped_item in self.equipped:
                    # if the player has an item equipped in that slot let them know to remove it
                    if equipped_item.body_part == item.body_part:
                        return "You have " + equipped_item.name + " equipped already, you must remove it first.\n"
                # Equip the item and remove from inventory
                self.equipped[item] = item.name
                del self.inventory[item]
                return "You have equipped " + item.name + ". \n"
        # if they had no matching items
        return "You don't have " + item_name + ". \n"

    def unequip_item(self, item_name):
        # check to see if the player has that item equipped
        for equipped_item in self.equipped:
            if item_name == equipped_item.name.lower():
                # item is equipped to remove it and place in inventory
                self.inventory[equipped_item] = item_name
                del self.equipped[equipped_item]
                return "You unequip " + item_name + " and place it in your inventory. \n"
        # player isn't wearing the item
        return "You are not wearing " + item_name + ". \n"

    def check_items(self, list_to_check):
        if list_to_check == "inventory":
            list_to_check = self.inventory
            reply = "You have these items in your inventory:\n"

        elif list_to_check == "equipment":
            list_to_check = self.equipped
            reply = "You have these items equipped:\n"

        for item in list_to_check:
            reply += item.name + "\n"

        return reply