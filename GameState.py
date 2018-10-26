from player import Player
#from room_sets import *
from item_sets import *
from Input_Parser.input_parser import *
from dataparse import *

class GameState:
    def __init__(self):
        self.main_player = Player()
        self.mansion = {}
        self.game_items = {}
        self.current_room = None

        self.json_Mansion = {}

    def build_item_sets(self):
        self.game_items["keys"] = Item(
            "keys", "Rusty golden key, looks like it could open anything.")


    def build_json_mansion(self):
        room_names = ["diningroom.json", "familyroom.json", "firstfloorfoyer.json", "garage.json", "grandroom.json",
                      "library.json", "mastersuite.json", "panicroom.json", "sarahsroom.json",
                      "secondfloorfoyer.json",
                      "study.json", "veranda.json", "basement.json", "secretroom.json", "winecellar.json"]
        for name in room_names:
            room_dict = inputData(name)
            new_room = Room(room_dict['location'], room_dict['long description'], room_dict['short description'],
                            room_dict['look at'], room_dict['exits'])

            self.json_Mansion[room_dict['location']] = new_room

        self.current_room = self.json_Mansion["First Floor Foyer"]

    def json_move(self, direction):
        if direction in self.current_room.exits:
            self.current_room.first_visit = False
            self.current_room = self.json_Mansion[self.current_room.exits[direction]]

    def move(self, direction):
        if direction in self.current_room.linked_rooms:
            self.current_room = self.current_room.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    def move_to(self, room_name):
        for key, value in self.current_room.linked_rooms.items():
            if value.name.lower() == room_name:
                self.current_room = value
                return self
        print("That room isn't connected to this one")
        return self

    def foyer_action_check(self, verb, noun):
        return

    def _show_game_items(self):
        print "There are %d game items" % len(self.game_items)
        for key, value in self.game_items.items():
            print key
            print value

    def _look_at(self, object_name):
        for key, value in self.current_room.features.items():
            if value.name.lower() == object_name:
                if value.hasAction:
                    self.action_check(self.current_room.name, object_name)
                else:
                    print value.get_description()
                return self
        print "The %s isn't in this room" % object_name
        return self

    def _add_to_inventory(self, object_name):
        for key, value in self.current_room.features.items():
            if value.name.lower() == object_name:
                self.current_room.take_item(self.game_items[object_name])
                self.main_player.take_item(self.game_items[object_name])
        return self
        print "The %s isn't in this room" % object_name

    def _process_cmd(self, cmd):

        #####################################################
        #   Process menu commands
        #####################################################
        if cmd.num_commands == 1:
            if cmd.command == 'exit':
                print "Thanks for playing!"
                exit()
            elif cmd.command == 'savegame':  # TODO: Implement save game
                print "Saving game..."
            elif cmd.command == 'loadgame':  # TODO: Implement load game
                print "Loading game..."
            elif cmd.command == 'inventory':
                self.check_inventory()
            elif cmd.command == 'showgameitems':
                self._show_game_items()

        #####################################################
        #   Process movement commands
        #####################################################
        elif cmd.num_directions == 1:
            #self.move(cmd.direction)
            self.json_move(cmd.direction)

        elif cmd.num_room_names == 1:
            self.move_to(cmd.room_name)

        #####################################################
        #   Process action commands
        #####################################################
        elif cmd.num_verbs == 1:
            if cmd.verb == 'look':
                # TODO: Implmenet:
                self._look_at(cmd.obj)
            elif cmd.verb == 'take' or cmd.verb == 'get' or cmd.verb == 'grab' or cmd.verb == 'pick up':
                # TODO: Implement:
                print 'GETTING %s' % cmd.obj
                self._add_to_inventory(cmd.obj)
            elif cmd.verb == 'put' or cmd.verb == 'use':
                # TODO: Implement:
                # get(parser.obj)    # should use the object if it's in the inventory
                print 'Using %s' % cmd.obj

    def play(self):

        cmd = Input_Parser()

        while True:
 #           print(self.current_room.get_details())
            if self.current_room.first_visit == True:
                print(self.current_room.long_description)
                self.current_room.first_visit == False
            else:
                print(self.current_room.short_description)
            cmd.get_input()
            self._process_cmd(cmd)

    def action_check(self, room_name, feature_name):
        if room_name.lower() == "foyer":
            if feature_name == "keys":
                print("Keys are now available in room")
                self.current_room.add_item(keys)

    def check_inventory(self):
        if bool(self.main_player.inventory) == False:
            print("There is nothing in your inventory")
        else:
            for items in self.main_player.inventory:
                print(items.name)
