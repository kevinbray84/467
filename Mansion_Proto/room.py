class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.description = "This is the " + room_name
        self.linked_rooms = {}

    def get_name(self):
        return self.name

    def set_description(self, room_description):
        self.description = room_description

    def get_description(self):
        return self.description

    def describe(self):
        print(self.get_description())

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
