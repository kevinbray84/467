class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = {}

    def take_item(self, item):
        self.inventory[item.name] = item

    def drop_item(self, item):
        del self.inventory[item]
