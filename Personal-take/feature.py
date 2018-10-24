
class Feature:
    def __init__(self, name, description=None, room_name=None):
        self.name = name
        self.description = description
        self.action = None
        self.searched = False
        self.linked_room = room_name
        self.hasAction = None

    def set_action(self, room_action):
        self.action = room_action()

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def action(self):
        return

    def has_action(self):
        self.hasAction = True








