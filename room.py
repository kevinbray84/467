from text_splitter import *


class Room:
    def __init__(self, room_name, long_description=None, short_description=None, look_at=None, exits=None):
        self.name = room_name
        self.long_description = long_description
        self.short_description = short_description
        self.look_at = look_at
        self.exits = exits
        self.linked_rooms = {}
        self.items_in_room = {}
        self.is_locked = True
        self.first_visit = True
        self.been_explored = False
        self.features = {}

    def get_name(self):
        return self.name

    def set_description(self, room_description):
        self.description = room_description

    def get_description(self):
        return self.long_description

    def get_secondary_description(self):
        if self.name == "Wine Cellar":
            if self.is_locked == True:
                return self.short_description['locked']
            else:
                return self.short_description['unlocked']
        elif self.name == "Library":
            if self.is_locked == True:
                return self.short_description['locked']
            else:
                return self.short_description['unlocked']
        elif self.name == "Master Suite":
            if self.is_locked == True:
                return self.short_description['not moved']
            else:
                return self.short_description['moved']
        elif self.name == 'Basement':
            if self.is_locked == True:
                return self.short_description['not used flashlight']
            else:
                return self.short_description['used flashlight']
        elif self.name == 'Secret Room':
            if self.is_locked == True:
                return self.short_description['not cut chain']
            else:
                return self.short_description['cut chain']
        return self.short_description

    def describe(self):
        if self.first_visit:
            print_split(self.get_description())
            self.first_visit = False
        else:
            print_split(self.get_secondary_description())

    def link_room(self, room_to_link, direction):
        self.linked_rooms[direction] = room_to_link

    def get_details(self):
        count = 1
        print("="*TEXT_WIDTH)
        print(self.get_name())
        print("="*TEXT_WIDTH)
        self.describe()
        has_gettable_items = False
        for key, value in self.items_in_room.items():  # check for getable items in room
            if value.is_getable == True:
                has_gettable_items = True
        if has_gettable_items:
            print("-"*TEXT_WIDTH)
            print("The following items are in the room:")

        for key, value in self.items_in_room.items():  # display all items that are getable
            if value.is_getable:
                print_split("%2d: %s: %s" %
                            (count, value.name, value.description))
                count += 1
        print("-"*TEXT_WIDTH)

        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print("The " + room.get_name() + " is " + direction)

    def move(self, direction):
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    def get_explore(self):
        if not self.been_explored:
            self.been_explored = True

    def add_feature(self, key, value):
        self.features[key] = value

    def add_item(self, item):
        self.items_in_room[item.name] = item

    def take_item(self, item):
        del self.items_in_room[item]
