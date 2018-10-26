class Item:
    def __init__(self, name=None, description=None, is_getable=True):
        self.name = name
        self.description = description
        self.is_getable = is_getable

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def get_item(self):
        return self.name

    def get_description(self):
        return self.description
