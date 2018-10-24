from room_sets import *


class Player:
    def __init__(self):
        self.current_room = foyer
        self.inventory = {}

    def move(self, direction):
        if direction in self.current_room.linked_rooms:
            self.current_room = self.current_room.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    def take_item(self, item):
        self.inventory[item.name] = item
