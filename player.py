from room_sets import *


class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = {}

    def take_item(self, item):
        self.inventory[item.name] = item
