class Room:
    def __init__(self, room_name, long_description=None, short_description=None, look_at=None, exits=None):
        self.name = room_name
        self.long_description = long_description
        self.short_description = short_description
        self.look_at = look_at
        self.exits = exits
        self.linked_rooms = {}
        self.items_in_room = {}
        self.is_locked = None
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
        return self.short_description

    def describe(self):
        if self.first_visit:
            print(self.get_description())
            self.first_visit = False
        else:
            print(self.get_secondary_description())

    def link_room(self, room_to_link, direction):
        self.linked_rooms[direction] = room_to_link

    def get_details(self):
        count = 1
        print("\n====================================================\n" + self.get_name())
        print("====================================================")
        self.describe()
        if len(self.items_in_room) > 0:
            print("----------------------------------------------------")
            print("\nThere are a few items in the room:")
        for key, value in self.items_in_room.items():
            print "%2d: %s: %s" % (count, value.name, value.description)
            count += 1
        print("----------------------------------------------------")
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print("The " + room.get_name() + " is " + direction)
        print 'ROOM DIRECTIONS COMPLETE'

    def move(self, direction):
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    # def set_explore(self, primary_desc, secondary_desc, ):

    def get_explore(self):
        if not self.been_explored:
            self.been_explored = True

    def add_feature(self, feature, curr_feature):
        self.features[feature] = curr_feature

    def add_item(self, item):
        self.items_in_room[item.name] = item
        print "Adding %s to %s... (%d)" % (
            item.name, self.name, len(self.items_in_room))

    def take_item(self, item):
        print 'REMOVING %s.  THERE ARE %d items before removing' % (
            item, len(self.items_in_room))
        del self.items_in_room[item]
        print 'REMOVED %s.  THERE ARE NOW %d items' % (
            item, len(self.items_in_room))
