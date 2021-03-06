from player import Player
from Input_Parser.input_parser import *
from dataparse import *
from item import *
import time
import sys
import os
from text_splitter import *
import pickle
import math


class GameState:
    def __init__(self):
        self.main_player = Player()
        self.game_items = {}
        self.current_room = None
        self.previous_room = None
        self.json_Mansion = {}
        self.build_json_mansion()
        self.add_items_to_mansion()
        self.link_json_mansion()
        self.is_new_game = True

        # these variables keep track of if object has been moved or observed before
        self.firstfloorfoyer_keys_taken = False
        self.diningroom_key_taken = False
        self.diningroom_flashlight_taken = False
        self.library_desk_slot_used = False
        self.library_panicroom_unlocked = False
        self.panicroom_video_watched = False
        self.garage_car_unlocked = False
        self.garage_boltcutters_taken = False
        self.familyroom_examinedcouch = False
        self.familyroom_code_taken = False
        self.familyroom_jacket_examined = False
        self.secondfloorfoyer_examineddrawers = False
        self.secondfloorfoyer_key_taken = False
        self.winecellar_wall_unlocked = False
        self.sarahsroom_diary_unlocked = False
        self.sarahsroom_diarykey_taken = False
        self.sarahsroom_bed_examined = False
        self.mastersuite_portrait_moved = False
        self.mastersuite_safe_unlocked = False
        self.mastersuite_safe_examined = False
        self.mastersuite_passphrase_taken = False
        self.basement_winecellar_found = False
        self.winecellar_keyhole = False
        self.secretroom_sarah_free = False
        self.secretroom_chain_broke = False

        self.last_command = ""

    """
    This function is called by the constructor and places all the items in each room.
    """
    def add_items_to_mansion(self):
        itemdict = inputData("items.json")
        keys = Item(itemdict["keys"]["name"],
                    itemdict["keys"]["description"], True)
        keys.set_use("correct", itemdict["keys"]["use"]["correct"])
        keys.set_use("incorrect", itemdict["keys"]["use"]["incorrect"])
        self.json_Mansion["First Floor Foyer"].add_item(keys)

        # not gettable until safe opens
        passphrase = Item(itemdict["passphrase"]["name"],
                          itemdict["passphrase"]["description"], False)
        passphrase.set_use("correct", itemdict["passphrase"]["use"]["correct"])
        passphrase.set_use(
            "incorrect", itemdict["passphrase"]["use"]["incorrect"])
        self.json_Mansion["Master Suite"].add_item(passphrase)

        # safe combination not getable until jacket is examined
        safe_combination = Item(
            itemdict["safe combination"]["name"], itemdict["safe combination"]["description"], False)
        safe_combination.set_use(
            "correct", itemdict["safe combination"]["use"]["correct"])
        safe_combination.set_use(
            "incorrect", itemdict["safe combination"]["use"]["incorrect"])
        self.json_Mansion["Family Room"].add_item(safe_combination)

        # bolt cutters are not getable until BMW trunk is opened
        bolt_cutters = Item(
            itemdict["bolt cutters"]["name"], itemdict["bolt cutters"]["description"], False)
        bolt_cutters.set_use(
            "correct", itemdict["bolt cutters"]["use"]["correct"])
        bolt_cutters.set_use(
            "incorrect", itemdict["bolt cutters"]["use"]["incorrect"])
        self.json_Mansion["Garage"].add_item(bolt_cutters)

        flashlight = Item(itemdict["flashlight"]["name"],
                          itemdict["flashlight"]["description"], True)
        flashlight.set_use("correct", itemdict["flashlight"]["use"]["correct"])
        flashlight.set_use(
            "incorrect", itemdict["flashlight"]["use"]["incorrect"])
        silver_key = Item(itemdict["silver key"]["name"],
                          itemdict["silver key"]["description"], True)
        silver_key.set_use("correct", itemdict["silver key"]["use"]["correct"])
        silver_key.set_use(
            "incorrect", itemdict["silver key"]["use"]["incorrect"])
        self.json_Mansion["Dining Room"].add_item(flashlight)
        self.json_Mansion["Dining Room"].add_item(silver_key)

        # engraved key is not getable until you look in the drawers
        engraved_key = Item(
            itemdict["engraved key"]["name"], itemdict["engraved key"]["description"], False)
        engraved_key.set_use(
            "correct", itemdict["engraved key"]["use"]["correct"])
        keys.set_use("incorrect", itemdict["engraved key"]["use"]["incorrect"])
        self.json_Mansion["Second Floor Foyer"].add_item(engraved_key)

        diary_key = Item(itemdict["diary key"]["name"],
                         itemdict["diary key"]["description"], False)
        diary_key.set_use("correct", itemdict["diary key"]["use"]["correct"])
        diary_key.set_use(
            "incorrect", itemdict["diary key"]["use"]["incorrect"])
        self.json_Mansion["Sarahs Room"].add_item(diary_key)

    """
    This function creates the rooms in the mansion by instantiatting room objects with
    data from the JSON files and placing the rooms in a dict.
    """
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

    """
    This function moves the player from one room to another using a cardinal direction.
    """
    def json_move(self, direction):
        if direction in self.current_room.exits:
            self.current_room.first_visit = False
            self.current_room = self.json_Mansion[self.current_room.exits[direction]]
            self.link_json_mansion()
        else:
            print_split("There should be a better way out of this room. Try leaving by a different direction.")

    """
    This function links the rooms in the mansion together.  It attempts to link each
    direction.  If there is an error linking, it means that there is nothing to
    link in that direction, so the exception handler simply passes.
    """
    def link_json_mansion(self):
        # link north
        try:
            self.current_room.link_room(
                self.json_Mansion[self.current_room.exits['north']], 'north')
        except KeyError:
            pass
        
        # link east
        # skip adding secret room exit to wine cellar until it's discovered    
        if self.current_room.name in {'Wine Cellar'}:
            print ""
        else:
            try:
                self.current_room.link_room(
                    self.json_Mansion[self.current_room.exits['east']], 'east')
            except KeyError:
                pass

        # link south
        # skip adding basement exit to wine cellar until it's discovered    
        if self.current_room.name in {'Basement'}:
            pass
        else:
            try:
                self.current_room.link_room(
                    self.json_Mansion[self.current_room.exits['south']], 'south')
            except KeyError:
                pass

        # link west   
        try:
            self.current_room.link_room(
                self.json_Mansion[self.current_room.exits['west']], 'west')
        except KeyError:
            pass


    # I'm not sure this ever gets called
    """
    def move(self, direction):
        if direction in self.current_room.linked_rooms:
            self.current_room = self.current_room.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self
    """

    """
    This function moves to a room by using the room name rather than a direction
    """
    def move_to(self, room_name):
        for key, value in self.current_room.linked_rooms.items():
            if value.name.lower() == room_name:
                self.current_room = value
                self.link_json_mansion()
                return self
        print("That room isn't connected to this one")
        return self

    """
    This function processes user commands that take place in the specified room
    """
    def _firstfloorfoyer_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'grand marble staircase', 'grand marble stair case','marble staircase', 'marble stair case', 'staircase','stair case','stairs', 'upstairs'}:
                cmd.direction = 'north'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'oak double doors', 'double doors', 'doors','oak doors'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'pillared entryway', 'pillared entry way', 'entryway', 'entry way', 'pillar entryway', 'pillar entry way', 'pillared', 'pillar'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
        
        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self
            elif object_name in {'mail', 'mailbox', 'stack of mail', 'stack'}:
                object_name = 'mail'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'keyholder','key holder','key holder on wall','key holders', 'key peg', 'key pegs','pegs',}:
                object_name = 'keyholder'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.firstfloorfoyer_keys_taken is False:
                        print_split(self.current_room.look_at[object_name]['keys not taken'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['keys taken'])
                        return self
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self

    """
    This function processes user commands that take place in the specified room
    """
    def _diningroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'carpeted step','step','carpet','carpeted steps','steps'}:
                cmd.direction = 'north'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'pillared entryway', 'pillared entry way', 'entryway', 'entry way', 'pillar entryway', 'pillar entry way', 'pillared', 'pillar'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'heavy wooden door','heavy door','wooden door','door'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
        
        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self
            elif object_name in {'foodtray', 'food', 'food tray', 'tray'}:
                object_name = 'food tray'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.diningroom_key_taken is False:
                        print_split(self.current_room.look_at[object_name]['key not taken'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['key taken'])
                        return self
            elif object_name in {'sidetable', 'side table', 'table'}:
                object_name = 'side table'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.diningroom_flashlight_taken is False:
                        print_split(self.current_room.look_at[object_name]['flashlight not taken'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['flashlight taken'])
                        return self
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self

    """
    This function processes user commands that take place in the specified room
    """
    def _library_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'rosewood sliding door', 'rosewood door','sliding door'}:
                cmd.direction = 'north'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'oak double doors', 'double doors', 'doors','oak doors'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
            elif self.library_panicroom_unlocked == True:
                if object_name in {'massive steel door', 'massive door', 'steel door'}:
                    cmd.direction = 'west'
                    self.json_move(cmd.direction)
                    return self
                else:
                    print("You don't seem to be able to move there.")
                    return self

        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self
            elif object_name in {'table', 'desk', 'tome', 'large tome'}:
                object_name = 'desk'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.library_desk_slot_used is False:
                        print_split(self.current_room.look_at[object_name]['untouched'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['used'])
                        return self
            elif object_name in {'panic room', 'panic door', 'panicroom', 'panic door', 'keypad', 'door'}:
                object_name = 'panic room'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.library_desk_slot_used is False:
                        # covers if trying to examine panic room without unlocking bookself
                        print_split("These actions don't seem possible in this room")
                        return self
                    elif self.library_panicroom_unlocked is False:
                        print_split(self.current_room.look_at[object_name]['locked'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['unlocked'])
                        return self
            elif object_name in {'statue', 'corner', 'sculpture'}:
                object_name = 'statue'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))

        elif cmd.verb in ['use', 'try', 'unlock', 'enter']:
            if object_name.lower() in {"engraved key"}:
                if self.main_player.inventory.has_key('engraved key'):
                    if self.library_desk_slot_used is False:
                        self.library_desk_slot_used = True
                        self.current_room.is_locked = False
                        print_split(self.main_player.inventory['engraved key'].use['correct'])

                    else:
                        print("You have already used the engraved key here")
                else:
                    print("You do not have the Coded Key in your inventory")


            elif cmd.verb in {'enter', 'use', 'try', 'activate'} and object_name.lower() in {'keypad'}:
                if self.library_desk_slot_used == False:
                    print "There is nothing to enter a code into"
                    return self
                code = raw_input("  Enter code to access safe> ")
                if code == 'NOPLACELIKEHOME':
                    print '  Access granted!'
                    print_split(self.main_player.inventory['passphrase'].use['correct'])
                    self.library_panicroom_unlocked = True
                    self.current_room.exits.update({"west": "Panic Room"})
                    self.current_room.linked_rooms['west'] = self.json_Mansion["Panic Room"]
                    response = raw_input("Would you like to enter now? > ")
                    if response.lower() in {"yes", "y"}:
                        self.json_move("west")
                    else:
                        return self
                else:
                    print '  Access denied.'
                    return self
            else:
                print("You try to use the {} but it seems to have no effect".format(object_name))
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self

    """
    This function processes user commands that take place in the specified room
    """
    def _garage_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'heavy wooden door','heavy door','wooden door','door'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self
            elif object_name in {'truck','pickup'}:
                object_name = 'truck'
            if self.current_room.look_at.has_key(object_name) == True:
                print_split(self.current_room.look_at[object_name])
                return self
            elif object_name in {'bmw','car','bmw car'}:
                object_name = 'BMW'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.garage_car_unlocked == False:
                        print_split(self.current_room.look_at[object_name]['locked'])
                        return self
                    elif self.garage_boltcutters_taken == False:
                        print_split(self.current_room.look_at[object_name]['unlocked']['bolt cutters not taken'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['unlocked']['bolt cutters taken'])
                        return self
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))

        if cmd.verb in {'unlock', 'use'}:
            if 'bmw' not in cmd.obj.lower() and 'car' not in cmd.obj.lower() and 'keys' not in cmd.obj.lower():
                print_split('You can\'t unlock the %s' % cmd.obj)
            elif self.main_player.inventory.has_key('keys'):
                if self.garage_car_unlocked == False:
                    print_split(self.main_player.inventory['keys'].use['correct'])
                    self.garage_car_unlocked = True
                    self.current_room.items_in_room['bolt cutters'].is_getable = True
                else:
                    print("The BMW car is already unlocked.")
            elif not self.main_player.inventory.has_key('keys'):
                print_split('You don\'t have the keys')
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self

    """
    This function processes user commands that take place in the specified room
    """
    def _familyroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'elegant wooden double french doors','wooden double french doors','double french doors','french doors','doors','elegant double french doors','elegant wooden doors','elegant french doors','wooden french doors'}:
                cmd.direction = 'north'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'solid oak door','oak door','oaken door', 'door'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'dimly lit staircase','dimly lit stair case','staircase','stair case','stairs', 'dimly lit stairs','downstairs'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'carpeted step','step','carpet','carpeted steps','steps'}:
                cmd.direction = 'south'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self
            elif object_name in {'billiards table','pool table', 'pooltable','table'}:
                object_name = 'billiards table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'couch','furniture', 'jacket', 'sofa'}:
                object_name = 'couch'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.familyroom_examinedcouch == False:
                        print_split(self.current_room.look_at[object_name]['before taking combination code'])
                        # self.familyroom_examinedcouch = True
                        return self
                    elif self.familyroom_code_taken == False:
                        print_split(self.current_room.look_at[object_name]['reexamining jacket before taking combination code'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['after taking combination code'])
                        return self
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))

        if cmd.verb == 'try on':
            if object_name in {'jacket', 'suit', 'suit jacket'}:
                object_name = 'couch'
            else:
                print_split('You can\'t try on the %s' % object_name)
                return self
            if self.familyroom_code_taken == False:
                if self.familyroom_jacket_examined == False:
                    print_split(self.current_room.look_at[object_name]['trying jacket on'])
                    self.familyroom_examinedcouch = True
                    self.familyroom_jacket_examined = True
                    self.current_room.items_in_room['safe combination'].is_getable = True
                else:
                    print_split(self.current_room.look_at[object_name]['trying on jacket second time'])
            elif self.familyroom_code_taken == True:
                print_split(self.current_room.look_at[object_name]['trying jacket on after taking combination'])
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _panicroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'massive steel door', 'massive door', 'steel door', 'door'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self

        if cmd.verb in {'look at', 'watch'}: 
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self       
            elif object_name in {'food','canned food','canned goods', 'water','bottled water','bottled waters'}:
                object_name = 'food'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'video','camera','video playback', 'monitors', 'monitor', 'video monitors', 'video monitor'}:
                object_name = 'video'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self   
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))

        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 
    
    """
    This function processes user commands that take place in the specified room
    """
    def _veranda_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'elegant wooden double french doors','wooden double french doors','double french doors','french doors','doors','elegant double french doors','elegant wooden doors','elegant french doors','wooden french doors'}:
                cmd.direction = 'south'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'sliding glass door','glass door','sliding door','door'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at': 
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self  
            elif object_name in {'patio table','padio table', 'patiotable','table', 'patio'}:
                object_name = 'patio table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'sky','storm','summer storm','clouds','storm in the sky'}:
                object_name = 'sky'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self        
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _study_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'oaken panel door', 'oaken door','panel door','oak door', 'oak panel door'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self
                
        if cmd.verb == 'look at': 
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self       
            elif object_name in {'computer', 'desktop', 'laptop','computer monitor'}:
                object_name = 'computer'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'mail', 'stack', 'stack of mail', 'desk'}:
                object_name = 'mail'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self        
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _secondfloorfoyer_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'decorated door','picture door','decorative door', 'door with pictures'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'oaken panel door', 'oaken door','panel door','oak door', 'oak panel door'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'grand marble staircase', 'grand marble stair case','marble staircase', 'marble stair case', 'staircase','stair case','stairs', 'downstairs'}:
                cmd.direction = 'south'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at':   
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print (value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self             
            elif object_name in {'table', 'table with drawers', 'newspaper', 'table top', 'drawer', 'drawers'}:
                object_name = 'table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
        elif cmd.verb == 'open':
            if object_name in {'drawers', 'drawer'}:
                object_name = 'drawers'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.secondfloorfoyer_examineddrawers == False:
                        print_split(self.current_room.look_at[object_name]['before taking key'])
                        self.secondfloorfoyer_examineddrawers = True
                        self.current_room.items_in_room['engraved key'].is_getable = True

                        return self
                    elif self.secondfloorfoyer_key_taken == False:
                        print_split(self.current_room.look_at[object_name]['reexamining without having taken key'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['after taking key'])
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _winecellar_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'opaque glass door','glass door','opaque door'}:
                cmd.direction = 'north'
                self.json_move(cmd.direction)
                return self
            elif self.winecellar_wall_unlocked == True:
                if object_name in {'disguised hidden stone door','hidden stone door','stone door','door','disguised stone door','disguised door','hidden door'}:
                    cmd.direction = 'east'
                    self.json_move(cmd.direction)
                    return self
                else:
                    print("You don't seem to be able to move there.")
                    return self

        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self          
            elif object_name in {'wine rack','wine','rack','wine racks','racks'}:
                object_name = 'wine rack'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'wall','bare wall','eastern wall','back wall'}:
                object_name = 'wall'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.winecellar_wall_unlocked is False:
                        print_split(self.current_room.look_at[object_name]['locked'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['unlocked'])
                        return self
            else:
                print_split("You can't examine the %s in the %s." % (object_name, self.current_room.name))

        elif cmd.verb in ['use', 'turn on', 'activate', 'unlock']:
            if object_name == 'flashlight':
                if object_name in self.main_player.inventory:
                    print_split(self.main_player.inventory['flashlight'].use['correct'])
                    self.winecellar_keyhole = True
                    return self
            if object_name == 'silver key':
                if object_name in self.main_player.inventory:
                    self.winecellar_wall_unlocked = True
                    print_split(self.main_player.inventory['silver key'].use['correct'])
                    self.current_room.is_locked = False # added to get around description print
                    self.current_room.exits.update({"east": "Secret Room"})
                    self.current_room.linked_rooms['east'] = self.json_Mansion["Secret Room"]
                    response = raw_input("Would you like to enter now? > ")
                    if response.lower() in {"yes", "y"}:
                        self.json_move("east")
                        return self
                    else:
                        return self
                else:
                    print_split("It appears you do not have this item")
            else:
                print "You can't %s the %s in the %s." % (cmd.verb, object_name, self.current_room.name)
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self

    """
    This function processes user commands that take place in the specified room
    """
    def _grandroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'sliding glass door','glass door','sliding door'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'intricately carved mahogany door', 'carved mahogany door','mahogany door','door','carved door', 'intricately carved door'}:
                cmd.direction = 'south'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at':
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print_split("Unable to look at object")
                    return self            
            elif object_name in {'fireplace','fire','fire place','ashes'}:
                object_name = 'fireplace'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'family portrait','portrait','family picture', 'family', 'picture'}:
                object_name = 'family portrait'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self    
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _secretroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'disguised hidden stone door','hidden stone door','stone door','door','disguised stone door','disguised door','hidden door'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at':  
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self        
            elif object_name in {'chain','chains','chain lock','lock','shackle'}:
                object_name = 'chain'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'sarah', 'daughter', 'her'}:
                object_name = 'sarah'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.secretroom_chain_broke == False:
                        print_split(self.current_room.look_at[object_name])
                        return self
                    else:
                        self.secretroom_sarah_free = True
                        print_split(self.current_room.look_at['sarah'])
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        if cmd.verb in ['use', 'cut']:
            if object_name in ['chain', 'chains', 'bolt cutters']:
                object_name = 'bolt cutters'
                if object_name in self.main_player.inventory:
                    print_split(self.main_player.inventory['bolt cutters'].use['correct'])
                    self.secretroom_chain_broke = True
                    self.current_room.is_locked = False
                    return self

        elif cmd.verb in ['rescue']:
            if object_name in ['sarah','daughter','her']:
                if self.secretroom_chain_broke == True:
                    end_text= "You have freed Sarah. You radio in your findings to a stunned watch commander before turning to Sarah. She seems a bit weak from her days of captivity so you wrap your coat around her and gently carry her out of the mansion. As you step outside into the rain, seeing the police lights flashing in the distance, you feel proud of your decision to trust your gut and vow to make sure the mayor and his wife pay for their actions. As the sirens get closer, you slowly begin to relax as you finally realize your journey has finally come to an end. CONGRATULATIONS YOU WIN "
                    print_split(end_text)
                    self.secretroom_sarah_free = True
                else:
                    print("Sarah is still chained. Need to cut it before you can rescue her.")
            else:
                print_split("The person or object you are trying to interact with does not seem to be in this room. Please try rescuing a different person.")

        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _sarahsroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'decorated door','picture door','decorative door', 'door with pictures'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self

        if cmd.verb in {'look at', 'look under'}:  
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self         
            elif object_name in {'side table','table','diary','sarahs diary','sarah\'s diary'}:
                object_name = 'side table'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.sarahsroom_diary_unlocked == False:
                        print_split(self.current_room.look_at[object_name]['locked'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['unlocked'])
                        return self
            elif object_name in {'bed', 'under bed','floor'}:
                object_name = 'bed'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.sarahsroom_bed_examined == False:
                        print_split(self.current_room.look_at[object_name]['not taken diary key'])
                        self.sarahsroom_bed_examined = True
                        self.current_room.items_in_room['diary key'].is_getable = True
                        return self
                    elif self.sarahsroom_diarykey_taken == False:
                        print_split(self.current_room.look_at[object_name]['reexamining not taken diary key'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['taken diary key'])
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)
        elif cmd.verb in {'open', 'read','unlock'}:
            if object_name == 'diary':
                object_name = 'diary'
                if self.sarahsroom_diary_unlocked == False:
                    if self.current_room.look_at.has_key("side table"):
                        if "diary key" in self.main_player.inventory:
                            self.sarahsroom_diary_unlocked = True
                            print_split(self.main_player.inventory['diary key'].use['correct'])
                        else:
                            print_split("The diary is locked.  Maybe there is a key somewhere?")
                elif self.sarahsroom_diary_unlocked == True:
                    print_split(self.current_room.look_at['side table']['unlocked'])



        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _mastersuite_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'intricately carved mahogany door', 'carved mahogany door','mahogany door', 'carved door', 'intricately carved door'}:
                cmd.direction = 'north'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'solid oak door','oak door','oaken door'}:
                cmd.direction = 'east'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'rosewood sliding door', 'rosewood door','sliding door'}:
                cmd.direction = 'south'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at': 
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self            
            elif object_name in {'portrait','portrait of the couple','portrait of couple'}:
                object_name = 'portrait'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.mastersuite_portrait_moved == False:
                        print_split(self.current_room.look_at[object_name]['not moved'])
                        return self
                    else:
                        print_split(self.current_room.look_at[object_name]['moved'])
                        return self
            elif object_name in {'safe', 'combination','hidden safe'}:
                object_name = 'safe'
                if self.mastersuite_portrait_moved == False:
                    print("These actions don't seem possible right now")
                    return self
                elif self.mastersuite_safe_unlocked == False:
                    print_split(self.current_room.look_at[object_name]['locked'])
                    return self
                elif self.mastersuite_safe_examined == False:
                    print_split(self.current_room.look_at[object_name]['unlocked'])
                    self.mastersuite_safe_examined = True
                    return self
                elif self.mastersuite_passphrase_taken == False:
                    print_split(self.current_room.look_at[object_name]['unlocked not taken passphrase'])
                    return self
                else:
                    print_split(self.current_room.look_at[object_name]['unlocked and taken'])
                    return self
            elif object_name in {'end table','small crystal containers','small crystal container','crystal containers','endtable'}:
                object_name = 'end table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)
        
        elif cmd.verb == 'move':
            if object_name in {'portrait','portrait of the couple','portrait of couple'}:
                object_name = 'portrait'
            else:
                print 'You can\'t move the %s' % object_name
                return self
            self.mastersuite_portrait_moved = True
            self.current_room.is_locked = False
            print_split(self.current_room.look_at[object_name]['moved'])

        elif cmd.verb in {'enter', 'open', 'use', 'unlock'} and cmd.obj in {'safe', 'code'}:
            if self.mastersuite_portrait_moved == False:
                print "There is nothing to enter a code into"
                return self
            code = raw_input("  Enter code to access safe> ")
            if code == '12-03-18':
                print '  Access granted!'
                self.mastersuite_safe_unlocked = True
                self.current_room.items_in_room['passphrase'].is_getable = True
                print_split(self.current_room.look_at['safe']['unlocked'])
                self.mastersuite_safe_examined = True
            else:
                print '  Access denied.'
                return self

        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self

    """
    This function processes user commands that take place in the specified room
    """
    def _basement_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'go' or cmd.verb == '':
            if object_name in {'dimly lit staircase','dimly lit stair case','staircase','stair case','stairs', 'dimly lit stairs','upstairs'}:
                cmd.direction = 'west'
                self.json_move(cmd.direction)
                return self
            elif object_name in {'opaque glass door','glass door','opaque door','door'}:
                cmd.direction = 'south'
                self.json_move(cmd.direction)
                return self

        if cmd.verb == 'look at':  
            if object_name in {'keys','passphrase','safe combination','bolt cutters','flashlight','silver key','engraved key','diary key'}:
                for key, value in self.current_room.items_in_room.items():
                    if value.name.lower() == object_name:
                        if value.is_getable:
                            print_split(value.description)
                            return self
                if self.main_player.inventory.has_key(object_name) == True:
                    for key,value in self.main_player.inventory.items():
                        if value.name.lower() == object_name:
                            print_split(value.description)
                            return self
                else:
                    print("Unable to look at object")
                    return self   
            elif object_name in {'trunk', 'large trunk'}:
                object_name = 'trunk'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self
            elif object_name in {'footprints','foot prints','footprint','foot print','ground','dust','floor'}:
                object_name = 'footprints'
                if self.current_room.look_at.has_key(object_name) == True:
                    print_split(self.current_room.look_at[object_name])
                    return self    
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        elif cmd.verb in ['use', 'turn on', 'activate']:
            object_name = cmd.obj
            if object_name.lower() == 'flashlight':
                print_split("You shine the light around the room and notice an opaque glass door previously shrouded in darkness on the south wall. It appears to lead to the Wine Cellar.  You also notice a trunk and some footprints.")
                self.current_room.exits.update({"south": "Wine Cellar"})
                self.current_room.linked_rooms['south'] = self.json_Mansion["Wine Cellar"]
                self.current_room.is_locked = False
            else:
                print "You can't use %s in the %s." % (object_name, self.current_room.name)
        else:
            if cmd.verb == "":
                print_split("You can\'t do that in the %s " % (self.current_room.name))

            else:
                print_split("You can\'t %s that in the %s " % (cmd.verb, self.current_room.name))
            return self 

    """
    This function processes user commands that take place in the specified room
    """
    def _add_to_inventory(self, object_name):
        for key, value in self.current_room.items_in_room.items():
            if value.name.lower() == object_name:
                if value.is_getable:
                    self.main_player.take_item(value)
                    self.current_room.take_item(key)
                    if value.name == 'keys':
                        self.firstfloorfoyer_keys_taken = True                    
                    elif value.name == 'safe combination':
                        self.familyroom_code_taken = True
                    elif value.name == 'passphrase':
                        self.mastersuite_passphrase_taken = True
                    elif value.name == 'silver key':
                        self.diningroom_key_taken = True
                    elif value.name == 'flashlight':
                        self.diningroom_flashlight_taken = True
                    elif value.name == 'bolt cutters':
                        self.garage_boltcutters_taken = True
                    elif value.name == 'diary key':
                        self.sarahroom_diarykey_taken = True
                    elif value.name == 'engraved key':
                        self.secondfloorfoyer_key_taken = True

                    if object_name[-1] == "s":
                        verb = "were"
                    else:
                        verb = "was"

                    print_split(object_name.capitalize() + " " + verb + " added to your inventory")
                else:
                    print "You can\'t get that item"
                return self
        print "The %s isn't in this room" % object_name

    """
    This function drops the specified item from the inventory into the current room.
    """
    def _drop_from_inventory(self, item_name):
        item_to_drop = self.main_player.inventory[item_name]
        self.main_player.drop_item(item_name)
        self.current_room.add_item(item_to_drop)
        print_split("{} has been dropped from your inventory".format(item_name))

    """
    This function displays the help menu
    """
    def _help(self):
        print "SYSTEM COMMANDS: "
        print "    savegame - saves the game"
        print "    loadgame - loads the game"
        print "    exit - exits the game"
        print "    look - refreshes the display of the current room's info"
        print "    help - displays this menu"
        print "NAVIGATION COMMANDS: "
        print "    go <direction> - move in the specified direction (north, south, east, west)"
        print "    go <room name> - move to the specified room"
        print "    go <exit name> - move to the room connected through the exit"
        print "    <exit name> - move to the room connected through the exit"
        print "    <direction> - move in the specified direction (north, south, east, west)"
        print "INVENTORY MANAGEMENT"
        print "    inventory - display's all items in the player's inventory"
        print "    get/take/grab/pick up <item name> - adds the specified item to inventory"
        print "    drop <item name> - drops the specified item in the current room"
        print "GAME ACTIONS"
        print "    unlock <object> - unlock the specified object"   
        print "    try <object> - attempt to use the specified object"   
        print "    move <object> - move the specified object"
        print "    enter code - enter the specified code"
        print "    try on <object> - wear the specified object"
        print "    open <object> - open the specified object"
        print "    activate <object> - start or turn on specified object"
        print "    cut <object> - cut the specified object"
        print "    read <object> - read the specified object"
        print "    watch <object> - watch the specified object"
        print "    talk to <character> - talk to a character"
        print "    rescue <character> - rescue the specified person"
        print "    look at <object> - examine an object"   
        print "    use <item name> - use the specified item"
        print "    turn on <item name> - turn on the specified item"


    """
    This function processes the user input and calls the appropriate game function
    """
    def _process_cmd(self, cmd):

        #####################################################
        #   Process menu commands
        #####################################################
        if cmd.num_commands == 1:
            if cmd.command == 'exit':
                print "Thanks for playing!"
                exit()
            elif cmd.command == 'inventory':
                self.check_inventory()
            elif cmd.command == 'help':
                self._help()
            elif cmd.command == 'look':
                self.last_command = 'look'

        #####################################################
        #   Process movement commands
        #####################################################
        elif cmd.num_directions == 1 and cmd.verb == 'go':
            self.last_command = "move"
            self.json_move(cmd.direction)

        elif cmd.num_room_names == 1 and cmd.verb == 'go':
            self.last_command = "move"
            self.move_to(cmd.room_name)

        elif cmd.num_directions == 1 and cmd.verb == '':
            self.last_command = "move"
            self.json_move(cmd.direction)
        #####################################################
        #   Process action commands
        #####################################################
        elif cmd.verb == 'take' or cmd.verb == 'get' or cmd.verb == 'grab' or cmd.verb == 'pick up':
            self.last_command = "take"
            self._add_to_inventory(cmd.obj)

        elif cmd.verb == 'drop':
            self.last_command = "drop"
            self._drop_from_inventory(cmd.obj)

        elif cmd.verb == 'talk to':
            if self.current_room.name.lower() == 'secret room':
                if cmd.obj in {'sarah', 'daughter', 'her'}:
                    print_split(self.current_room.look_at['sarah'])
                else:
                    print("This person does not appear to be within this room.") 
            else:
                print("There does not appear to be anyone to talk with in this room.") 

        elif self.current_room.name.lower() == 'first floor foyer':
            self._firstfloorfoyer_features(cmd)
        elif self.current_room.name.lower() == 'dining room':
            self._diningroom_features(cmd)
        elif self.current_room.name.lower() == 'garage':
                self._garage_features(cmd)
        elif self.current_room.name.lower() == 'library':
            self._library_features(cmd)       
        elif self.current_room.name.lower() == 'family room':
            self._familyroom_features(cmd)
        elif self.current_room.name.lower() == 'panic room':
            self._panicroom_features(cmd)    
        elif self.current_room.name.lower() == 'veranda':
            self._veranda_features(cmd)
        elif self.current_room.name.lower() == 'study':
            self._study_features(cmd)    
        elif self.current_room.name.lower() == 'second floor foyer':
            self._secondfloorfoyer_features(cmd)
        elif self.current_room.name.lower() == 'wine cellar':
            self._winecellar_features(cmd)                  
        elif self.current_room.name.lower() == 'grand room':
            self._grandroom_features(cmd)
        elif self.current_room.name.lower() == 'secret room':
            self._secretroom_features(cmd)         
        elif self.current_room.name.lower() == 'sarahs room':
            self._sarahsroom_features(cmd)
        elif self.current_room.name.lower() == 'master suite':
            self._mastersuite_features(cmd)    
        elif self.current_room.name.lower() == 'basement':
            self._basement_features(cmd)
                                    
        else:
            print 'DEFAULT: You can\'t %s in the %s' % (cmd.verb, self.current_room.name)
            

    """
    This function displayes the player's current inventory
    """  
    def check_inventory(self):
        if bool(self.main_player.inventory) == False:
            print("There is nothing in your inventory")
        else:
            counter = 1
            print("The inventory contains %d items:") % len(self.main_player.inventory)
            for key, value in self.main_player.inventory.items():
                print_split("%2d: %s - %s" % (counter, value.name, value.description))
                counter += 1
        print("")

    """
    This function displays the current room information
    """
    def _render_room(self):
        self.current_room.get_details()

    """
    This function displays opening text crawl
    """
    def beginning_text(self):
        clear_terminal()
        title_width = len(" _____ _                                   _             ")
        side_bit = int(math.floor(((TEXT_WIDTH / 2) - math.ceil(title_width/2))))

        title = [
            "#" * TEXT_WIDTH,
            " _____ _                                   _             ",
            "/__   \ |__   ___    /\/\   __ _ _ __  ___(_) ___  _ __  ",
            "  / /\/ '_ \ / _ \  /    \ / _` | '_ \/ __| |/ _ \| '_ \ ",
            " / /  | | | |  __/ / /\/\ \ (_| | | | \__ \ | (_) | | | |",
            " \/   |_| |_|\___| \/    \/\__,_|_| |_|___/_|\___/|_| |_|",
            "                                                         ",
            "#" * TEXT_WIDTH,

        ]

        for i, lines in enumerate(title, 0):
            if i == 0 or i == len(title)-1:
                print(lines)
            else:
                print("{}{}{}".format(' ' * side_bit, lines, ' ' * side_bit))

        time.sleep(.5)

        print("")

        text_main = "Its a dark and stormy night. Looking up through the oak tree branches, you see a storm brewing overhead. The cloudy sky seems to mirror the inner turmoil you are currently feeling. Almost subconsciously, your hand reaches into your pocket to touch your detective badge. From its presence, you seem to find renewed determination and resolve within yourself. As you wait in the shadow of the tree, watching the mansion across the field, you reflect on what a whirlwind the last few days have been. Several days ago, the mayors daughter, Sarah, was kidnapped. Over the course of your investigation, you began to feel that something was off with this case. There were simply too many aspects that didnt add up. A crazy thought began to form in the back of your mind. Maybe this wasnt just some high-profile kidnapping, maybe, this was an inside job. Perhaps this poor little girl was right under everyones noses, in the mayors mansion. You know no one would believe you, but you cant just sit on the sidelines any more. There must be some clues hidden within the mansion, and you intend to find them. Sudden movement of the garage door snaps you out of your thoughts. You see the Mayor and his wife pull out of the driveway in one of their many cars and head off into town. Now or never you tell yourself. You quickly cross the field and make your way to the door. You lockpick the front door and step inside the mansion."

        text_secondary = "Good Luck..."

        new_text = split_input(text_main, TEXT_WIDTH)
        animate_text(new_text, 0.01)

        time.sleep(1)

        print("\n")

        new_secondary = split_input(text_secondary, TEXT_WIDTH)
        animate_text(new_secondary, 0.25)

        time.sleep(2)

    """
    This function starts the main loop of the game.  It returns 3 status flags:
    1) savegame - has the user selected the savaegame option?
    2) loadgame - has the user selected the loadgame option?
    3) donegame - has the user finished the game?
    """
    def play(self):
        cmd = Input_Parser()
        self.main_player.current_room = self.json_Mansion["First Floor Foyer"]
        self.previous_room = None

        #########################################
        # Main Loop
        #########################################

        if self.is_new_game:
            self.beginning_text()
            self.is_new_game = False
            
        while self.secretroom_sarah_free == False:

            if self.current_room != self.previous_room:
                self._render_room()
                self.previous_room = self.current_room

            if self.last_command == "look":
                self._render_room()
                self.last_command = ""
                
            print("")
            cmd.get_input()
            if cmd.command == 'savegame': 
                return True, False, False
            if cmd.command == 'loadgame':  
                return False, True, False

            self._process_cmd(cmd)
        
        return False, False, True # return victory flag after exiting loop
