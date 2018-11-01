from player import Player
from Input_Parser.input_parser import *
from dataparse import *
from item import *
import time
import sys
import os
from text_splitter import *


class GameState:
    def __init__(self):
        self.main_player = Player()
        # self.mansion = {}
        self.game_items = {}
        self.current_room = None
        self.json_Mansion = {}
        self.build_json_mansion()
        self.add_items_to_mansion()
        self.link_json_mansion()
# these variables keep track of if object has been moved or observed before
        self.firstfloorfoyer_keys_taken = False
#        self.add_json_mansion_features()

    def add_items_to_mansion(self):
        itemdict = inputData("items.json")
        keys = Item(itemdict["keys"]["name"], itemdict["keys"]["description"], True)
        keys.set_use("correct", itemdict["keys"]["use"]["correct"])
        keys.set_use("incorrect", itemdict["keys"]["use"]["incorrect"])
        self.json_Mansion["First Floor Foyer"].add_item(keys)

        # not gettable until safe opens
        passphrase = Item(itemdict["passphrase"]["name"], itemdict["passphrase"]["description"], False)
        passphrase.set_use("correct", itemdict["passphrase"]["use"]["correct"])
        passphrase.set_use("incorrect", itemdict["passphrase"]["use"]["incorrect"])
        self.json_Mansion["Master Suite"].add_item(passphrase)

        # not getable until jacket is examined
        safe_combination = Item(itemdict["safe combination"]["name"], itemdict["safe combination"]["description"], False)
        safe_combination.set_use("correct", itemdict["safe combination"]["use"]["correct"])
        safe_combination.set_use("incorrect", itemdict["safe combination"]["use"]["incorrect"])
        self.json_Mansion["Family Room"].add_item(safe_combination)

        # not getable until BMW trunk is opened
        bolt_cutters = Item(itemdict["bolt cutters"]["name"], itemdict["bolt cutters"]["description"], True)
        bolt_cutters.set_use("correct", itemdict["bolt cutters"]["use"]["correct"])
        bolt_cutters.set_use("incorrect", itemdict["bolt cutters"]["use"]["incorrect"])
        self.json_Mansion["Garage"].add_item(bolt_cutters)

        flashlight = Item(itemdict["flashlight"]["name"], itemdict["flashlight"]["description"], True)
        flashlight.set_use("correct", itemdict["flashlight"]["use"]["correct"])
        flashlight.set_use("incorrect", itemdict["flashlight"]["use"]["incorrect"])
        silver_key = Item(itemdict["silver key"]["name"], itemdict["silver key"]["description"], True)
        silver_key.set_use("correct", itemdict["keys"]["use"]["correct"])
        silver_key.set_use("incorrect", itemdict["keys"]["use"]["incorrect"])
        self.json_Mansion["Dining Room"].add_item(flashlight)
        self.json_Mansion["Dining Room"].add_item(silver_key)

        # not getable until you look in the drawers
        engraved_key = Item(itemdict["engraved key"]["name"], itemdict["engraved key"]["description"], True)
        engraved_key.set_use("correct", itemdict["engraved key"]["use"]["correct"])
        keys.set_use("incorrect", itemdict["engraved key"]["use"]["incorrect"])
        self.json_Mansion["Second Floor Foyer"].add_item(engraved_key)

        diary_key = Item(itemdict["diary key"]["name"], itemdict["diary key"]["description"], True)
        diary_key.set_use("correct", itemdict["diary key"]["use"]["correct"])
        diary_key.set_use("incorrect", itemdict["diary key"]["use"]["incorrect"])
        self.json_Mansion["Sarah's Room"].add_item(diary_key)

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

# I realized I didn't need to populate a features dict as the look_at parameter of the room class can act as a dict
#    def add_json_mansion_features(self):
#        self.json_Mansion['First Floor Foyer'].add_feature('mail', self.json_Mansion['First Floor Foyer'].look_at['mail'])
#        self.json_Mansion['First Floor Foyer'].add_feature('keys', {})
#        self.json_Mansion['First Floor Foyer'].features['keys']['keys not taken'] = self.json_Mansion['First Floor Foyer'].look_at['keys']['keys not taken']
#        self.json_Mansion['First Floor Foyer'].features['keys']['keys taken'] = self.json_Mansion['First Floor Foyer'].look_at['keys']['keys taken']

#        self.json_Mansion['Dining Room'].add_feature('food tray', {})
#        self.json_Mansion['Dining Room'].add_feature('side table', {})
#        self.json_Mansion['Dining Room'].features['food tray']['key not taken'] = self.json_Mansion['Dining Room'].look_at['food tray']['key not taken']    
#        self.json_Mansion['Dining Room'].features['food tray']['key taken'] = self.json_Mansion['Dining Room'].look_at['food tray']['key taken'] 
#        self.json_Mansion['Dining Room'].features['side table']['flashlight not taken'] = self.json_Mansion['Dining Room'].look_at['side table']['flashlight not taken']    
#        self.json_Mansion['Dining Room'].features['side table']['flashlight taken'] = self.json_Mansion['Dining Room'].look_at['side table']['flashlight taken'] 

#        for key, value in self.json_Mansion['First Floor Foyer'].features.items():
#            print key
#            print value
            

    def json_move(self, direction):
        if direction in self.current_room.exits:
            self.current_room.first_visit = False
            self.current_room = self.json_Mansion[self.current_room.exits[direction]]
            self.link_json_mansion()

    def link_json_mansion(self):
        try:
            self.current_room.link_room(
                self.json_Mansion[self.current_room.exits['north']], 'north')
        except KeyError:
            pass
        try:
            self.current_room.link_room(
                self.json_Mansion[self.current_room.exits['east']], 'east')
        except KeyError:
            pass
        try:
            self.current_room.link_room(
                self.json_Mansion[self.current_room.exits['south']], 'south')
        except KeyError:
            pass
        try:
            self.current_room.link_room(
                self.json_Mansion[self.current_room.exits['west']], 'west')
        except KeyError:
            pass

    def move(self, direction):
        if direction in self.current_room.linked_rooms:
            self.current_room = self.current_room.linked_rooms[direction]
        else:
            print("You can't go that way")
            raw_input("Press enter to continue...")
            return self

    def move_to(self, room_name):
        for key, value in self.current_room.linked_rooms.items():
            if value.name.lower() == room_name:
                self.current_room = value
                self.link_json_mansion()
                return self
        print("That room isn't connected to this one")
        raw_input("Press enter to continue...")
        return self

    def foyer_action_check(self, verb, noun):
        return

    def _show_game_items(self):
        print "There are %d game items" % len(self.game_items)
        for key, value in self.game_items.items():
            print key
            print value
# old look_at
#    def _look_at(self, object_name):
#        for key, value in self.current_room.features.items():
#            if value.name.lower() == object_name:
#                if value.hasAction:
#                    self.action_check(self.current_room.name, object_name)
#                else:
#                    print value.get_description()
#                return self
#        print "The %s isn't in this room" % object_name
#        raw_input("Press any key to continue...")
#        return self

    def _look_at(self, object_name):
        print("successfully called look at function")
        print("object: " + object_name.obj)
        if self.current_room.name == 'First Floor Foyer':
            self._firstfloorfoyer_features(object_name)
        else:
            print("These actions don't seem possible in this room")
        return self
# I am thinking of having a separate function for each room to cover all the scenarios
# since the room data can't be standardized
    def _firstfloorfoyer_features(self, object_name):
        if object_name.obj in {'mail', 'mailbox'}:
            object_name.obj = 'mail'
            if self.current_room.look_at.has_key(object_name.obj) == True:
                print self.current_room.look_at[object_name.obj]
                return self
        elif object_name.obj in {'keys', 'key peg'}:
            object_name.obj = 'keys'
            if self.current_room.look_at.has_key(object_name.obj) == True:
                if self.firstfloorfoyer_keys_taken is False:
                    print self.current_room.look_at[object_name.obj]['keys not taken']
                    return self
                else:
                    print self.current_room.look_at[object_name.obj]['keys taken']
                    return self
        else:
            print("These actions don't seem possible in this room")
            return self

    def _add_to_inventory(self, object_name):
        for key, value in self.current_room.items_in_room.items():
            print key
            print value
            if value.name.lower() == object_name:
                self.main_player.take_item(value)
                self.current_room.take_item(key)
                return self
        print "The %s isn't in this room" % object_name
        raw_input("Press enter to continue...")

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
            elif cmd.command == 'show inventory':
                self.check_inventory()
            elif cmd.command == 'showgameitems':
                self._show_game_items()

        #####################################################
        #   Process movement commands
        #####################################################
        elif cmd.num_directions == 1:
            # self.move(cmd.direction)
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
                self._add_to_inventory(cmd.obj)
            elif cmd.verb == 'put' or cmd.verb == 'use':
                # TODO: Implement:
                # get(parser.obj)    # should use the object if it's in the inventory
                print 'Using %s' % cmd.obj

    def play(self):

        cmd = Input_Parser()

        self.main_player.current_room = self.json_Mansion["First Floor Foyer"]

        #########################################
        # Main Loop
        #########################################
        #self.beginning_text()
        while True:
            clear_terminal()
            self._render_room()
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
            counter = 1
            print("The inventory contains %d items:") % len(
                self.main_player.inventory)
            for key, value in self.main_player.inventory.items():
                print "%2d: %s" % (counter, value.name)
                counter += 1
        raw_input("Press enter to continue...")

    def _render_room(self):
        print(self.current_room.get_details())

    def beginning_text(self):
        prompt_width = 90
        text_width = 80
        text_main = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        text_secondary = "Good Luck..."

        for i, letter in enumerate(text_main):
            sys.stdout.write(letter)
            time.sleep(0.02)
            if i % 80 == 0 and i != 0:
                sys.stdout.write("\n")

        time.sleep(1)
        print("\n")
        for i, letter in enumerate(text_secondary):
            sys.stdout.write(letter)
            time.sleep(.25)
            if i == 80:
                sys.stdout.write("\n")

        time.sleep(2)
        clear_terminal()
        return
