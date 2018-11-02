class Item:
    def __init__(self, name, description, is_getable=True):
        self.name = name
        self.description = description
        self.use = {}
        self.is_getable = is_getable

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_use(self, key, value):
        self.use[key] = value

    def get_item(self):
        return self.name

    def get_description(self):
        return self.description
