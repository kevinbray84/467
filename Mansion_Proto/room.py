class Room:
    def __init__(self, room_name, locked_status=False):
        self.name = room_name
        self.description = "This is the " + room_name
        self.secondary_description = "This is the " + room_name + "'s secondary description"
        self.linked_rooms = {}
        self.items_in_room = {}
        self.is_locked = locked_status
        self.first_visit = True
        self.been_explored = False

    def get_name(self):
        return self.name

    def set_description(self, room_description):
        self.description = room_description

    def get_description(self):
        return self.description

    def get_secondary_description(self):
        return self.secondary_description

    def describe(self):
        if self.first_visit:
            print(self.get_description())
            self.first_visit = False
        else:
            print(self.get_secondary_description())

    def link_room(self, room_to_link, direction):
        self.linked_rooms[direction] = room_to_link

    def get_details(self):
        print("\n====================================================\n" + self.get_name())
        print("====================================================")
        self.describe()
        print("----------------------------------------------------")
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print("The " + room.get_name() + " is " + direction)

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
