from room_sets import *


class Player:
    def __init__(self):
        self.current_room = foyer

    def move(self, direction):
        print "DIRECTION: %s" % direction
        if direction in self.current_room.linked_rooms:
            self.current_room = self.current_room.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    def move_to(self, room):
        for key, value in self.current_room.linked_rooms.items():
            if value.name.lower() == room:
                self.current_room = value
                return self
        print("That room isn't connected to this one")
        return self
