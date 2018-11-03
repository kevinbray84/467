class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = {}

    def take_item(self, item):
        if item.is_getable:
            self.inventory[item.name] = item
        else:
            print 'You can\'t get that item'

    def drop_item(self, item):
        del self.inventory[item]
