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
        self.diningroom_key_taken = False
        self.diningroom_flashlight_taken = False
        self.library_desk_slot_used = False
        self.library_panicroom_unlocked = False
        self.garage_car_unlocked = False
        self.garage_boltcutters_taken = False
        self.familyroom_examinedcouch = False
        self.familyroom_code_taken = False
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

        self.last_command = ""


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
        bolt_cutters = Item(itemdict["bolt cutters"]["name"], itemdict["bolt cutters"]["description"], False)
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
        self.json_Mansion["Sarahs Room"].add_item(diary_key)

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


    # def _look_at(self, cmd):
    #     #print("successfully called look at function")
    #     # print("object: " + self.current_room.items_in_room[object_name].name)
    #     if self.current_room.name == 'First Floor Foyer':
    #         self._firstfloorfoyer_features(cmd)
    #     elif self.current_room.name == 'Dining Room':
    #         self._diningroom_features(cmd)
    #     elif self.current_room.name == 'Library':
    #         self._library_features(cmd)
    #     elif self.current_room.name == 'Garage':
    #         self._garage_features(cmd)
    #     elif self.current_room.name == 'Family Room':
    #         self._familyroom_features(cmd)
    #     elif self.current_room.name == 'Panic Room':
    #         self._panicroom_features(cmd)
    #     elif self.current_room.name == 'Veranda':
    #         self._veranda_features(cmd)
    #     elif self.current_room.name == 'Study':
    #         self._study_features(cmd)
    #     elif self.current_room.name == 'Second Floor Foyer':
    #         self._secondfloorfoyer_features(cmd)
    #     elif self.current_room.name == 'Wine Cellar':
    #         self._winecellar_features(cmd)
    #     elif self.current_room.name == 'Grand Room':
    #         self._grandroom_features(cmd)
    #     elif self.current_room.name == 'Secret Room':
    #         self._secretroom_features(cmd)
    #     elif self.current_room.name == "Sarahs Room":
    #         self._sarahsroom_features(cmd)
    #     elif self.current_room.name == 'Master Suite':
    #         self._mastersuite_features(cmd)
    #     elif self.current_room.name == 'Basement':
    #         self._basement_features(cmd)
    #     else:
    #         print("These actions don't seem possible in this room")
    #     return self

    def _firstfloorfoyer_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':
            if object_name in {'mail', 'mailbox'}:
                object_name = 'mail'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'keys', 'key peg'}:
                object_name = 'keys'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.firstfloorfoyer_keys_taken is False:
                        print self.current_room.look_at[object_name]['keys not taken']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['keys taken']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)
        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self

    def _diningroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':
            if object_name in {'foodtray', 'food', 'food tray', 'tray'}:
                object_name = 'food tray'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.diningroom_key_taken is False:
                        print self.current_room.look_at[object_name]['key not taken']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['keys taken']
                        return self
            elif object_name in {'sidetable', 'side table', 'table'}:
                object_name = 'side table'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.diningroom_flashlight_taken is False:
                        print self.current_room.look_at[object_name]['flashlight not taken']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['flashlight taken']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)
        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self

    def _library_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':
            if object_name in {'desk', 'tome', 'large tome'}:
                object_name = 'desk'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.library_desk_slot_used is False:
                        print self.current_room.look_at[object_name]['untouched']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['used']
                        return self
            elif object_name in {'panic room', 'panic door', 'panicroom', 'panic door', 'keypad'}:
                object_name = 'panic room'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.library_desk_slot_used is False:
                        #covers if trying to examine panic room without unlocking bookself
                        print("These actions don't seem possible in this room")
                        return self
                    elif self.library_panicroom_unlocked is False:
                        print self.current_room.look_at[object_name]['locked']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['unlocked']
                        return self
            elif object_name in {'statue', 'corner', 'sculpture'}:
                object_name = 'statue'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)
        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self

    def _garage_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':
            if object_name in {'truck','pickup'}:
                object_name = 'truck'
            if self.current_room.look_at.has_key(object_name) == True:
                print self.current_room.look_at[object_name]
                return self
            elif object_name in {'bmw','car','bmw car'}:
                object_name = 'BMW'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.garage_car_unlocked == False:
                        print self.current_room.look_at[object_name]['locked']
                        return self
                    elif self.garage_boltcutters_taken == False:
                        print self.current_room.look_at[object_name]['unlocked']['bolt cutters not taken']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['unlocked']['bolt cutters taken']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        if cmd.verb == 'unlock':
            if 'bmw' not in cmd.obj.lower() and 'car' not in cmd.obj.lower():
                print 'You can\'t unlock the %s' % cmd.obj
            elif self.main_player.inventory.has_key('keys'):
                print self.main_player.inventory['keys'].use['correct']
                self.garage_car_unlocked = True
                self.current_room.items_in_room['bolt cutters'].is_getable = True
            elif not self.main_player.inventory.has_key('keys'):
                print 'You don\'t have the keys'
        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self

    def _familyroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':
            if object_name in {'billiards table','pool table', 'pooltable','table'}:
                object_name = 'billiards table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'couch','furniture', 'jacket', 'sofa'}:
                object_name = 'couch'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.familyroom_examinedcouch == False:
                        print self.current_room.look_at[object_name]['before taking combination code']
                        self.familyroom_examinedcouch = True
                        return self
                    elif self.familyroom_code_taken == False:
                        print self.current_room.look_at[object_name]['reexamining jacket before taking combination code']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['after taking combination code']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _panicroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':        
            if object_name in {'food','canned food','canned goods', 'water','bottled water','bottled waters'}:
                object_name = 'food'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'video','camera','video playback', 'monitors', 'monitor', 'video monitors', 'video monitor'}:
                object_name = 'video'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self   
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 
    
    def _veranda_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':   
            if object_name in {'patio table','padio table', 'patiotable','table', 'patio'}:
                object_name = 'patio table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'sky','storm','summer storm','clouds','storm in the sky'}:
                object_name = 'sky'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self        
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _study_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':        
            if object_name in {'computer', 'desktop', 'laptop','computer monitor'}:
                object_name = 'computer'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'mail', 'stack', 'stack of mail', 'desk'}:
                object_name = 'mail'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self        
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _secondfloorfoyer_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':                
            if object_name in {'table', 'table with drawers', 'newspaper', 'table top'}:
                object_name = 'table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'drawers', 'drawer'}:
                object_name = 'drawers'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.secondfloorfoyer_examineddrawers == False:
                        print self.current_room.look_at[object_name]['before taking key']
                        self.secondfloorfoyer_examineddrawers = True
                        return self
                    elif self.secondfloorfoyer_key_taken == False:
                        print self.current_room.look_at[object_name]['reexamining without having taken key']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['after taking key']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _winecellar_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':          
            if object_name in {'wine rack','wine','rack'}:
                object_name = 'wine rack'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'wall','bare wall','eastern wall','back wall'}:
                object_name = 'wall'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.winecellar_wall_unlocked is False:
                        print self.current_room.look_at[object_name]['locked']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['unlocked']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self

    def _grandroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':            
            if object_name in {'fireplace','fire','fire place','ashes'}:
                object_name = 'fireplace'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'family portrait','portrait','family picture', 'family', 'picture'}:
                object_name = 'family portrait'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self    
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _secretroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':          
            if object_name in {'chain','chains','chain lock','lock','shackle'}:
                object_name = 'chain'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'sarah','daughter','her'}:
                object_name = 'sarah'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self       
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _sarahsroom_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':           
            if object_name in {'side table','table','diary','sarahs diary','sarah\'s diary'}:
                object_name = 'side table'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.sarahsroom_diary_unlocked == False:
                        print self.current_room.look_at[object_name]['locked']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['unlocked']
                        return self
            elif object_name in {'bed', 'under bed','floor'}:
                object_name = 'bed'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.sarahsroom_bed_examined == False:
                        print self.current_room.look_at[object_name]['not taken diary key']
                        self.sarahsroom_bed_examined = True
                        return self
                    elif self.sarahsroom_diarykey_taken == False:
                        print self.current_room.look_at[object_name]['reexamining not taken diary key']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['taken diary key']
                        return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 

    def _mastersuite_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':             
            if object_name in {'portrait','portrait of the couple','portrait of couple'}:
                object_name = 'portrait'
                if self.current_room.look_at.has_key(object_name) == True:
                    if self.mastersuite_portrait_moved == False:
                        print self.current_room.look_at[object_name]['not moved']
                        return self
                    else:
                        print self.current_room.look_at[object_name]['moved']
                        return self
            elif object_name in {'safe', 'combination','hidden safe'}:
                object_name = 'safe'
                if self.mastersuite_portrait_moved == False:
                    print("These actions don't seem possible right now")
                    return self
                elif self.mastersuite_safe_unlocked == False:
                    print self.current_room.look_at[object_name]['locked']
                    return self
                elif self.mastersuite_safe_examined == False:
                    print self.current_room.look_at[object_name]['unlocked']
                    self.mastersuite_safe_examined = True
                    return self
                elif self.mastersute_passphrase_taken == False:
                    print self.current_room.look_at[object_name]['unlocked not taken passphrase']
                    return self
                else:
                    print self.current_room.look_at[object_name]['unlocked and taken']
                    return self
            elif object_name in {'end table','small crystal containers','small crystal container','crystal containers','endtable'}:
                object_name = 'end table'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self

    def _basement_features(self, cmd):
        object_name = cmd.obj
        if cmd.verb == 'look at':     
            if object_name in {'trunk', 'large trunk'}:
                object_name = 'trunk'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self
            elif object_name in {'footprints','foot prints','footprint','foot print','ground','dust','floor'}:
                object_name = 'footprints'
                if self.current_room.look_at.has_key(object_name) == True:
                    print self.current_room.look_at[object_name]
                    return self    
            else:
                print "You can't examine the %s in the %s." % (object_name, self.current_room.name)

        else:
            print("These actions don't seem possible in the %s " % self.current_room.name)
            return self 


    def _add_to_inventory(self, object_name):
        for key, value in self.current_room.items_in_room.items():
            if value.name.lower() == object_name:
                if value.is_getable:
                    self.main_player.take_item(value)
                    self.current_room.take_item(key)
                    if value.name == 'keys':
                        self.firstfloorfoyer_keys_taken = True
                else:
                    print "You can\'t get that item"
                return self
        print "The %s isn't in this room" % object_name
        raw_input("Press enter to continue...")

    def _drop_from_inventory(self, item_name):
        item_to_drop = self.main_player.inventory[item_name]
        self.main_player.drop_item(item_name)
        self.current_room.add_item(item_to_drop)
        raw_input("Press enter to continue...")

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
        print "INVENTORY MANAGEMENT"
        print "    show inventory - display's all items in the player's inventory"
        print "    get <item name> - adds the specified item to inventory"
        print "    drop <item name> - drops the specified item in the current room"
        print "GAME ACTIONS"
        print "    look at <item name> - examine an object"   
        print "    unlock <item name> - unlock the specified item"   
        print "    try on <item name> - wear the specified item"
        print "    move <item name> - move the specified item"
        print "    open <item name> - open the specified item"
        print "    enter <code> - enter the specified code"
        print "    watch <item name> - watch the specified item"
        print "    turn on <item name> - turn on the specified item"
        print "    use <item name> - use the specified item"
        print "    cut <item name> - cut the specified item"
        print "    rescue <character name> - rescue the specified person"
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

        #####################################################
        #   Process action commands
        #####################################################
        elif cmd.num_verbs == 1:
            # if cmd.verb == 'look at':
            #     self.last_command = "look at"
            #     self._look_at(cmd)
            if cmd.verb == 'take' or cmd.verb == 'get' or cmd.verb == 'grab' or cmd.verb == 'pick up':
                self.last_command = "take"
                self._add_to_inventory(cmd.obj)
            elif cmd.verb == 'drop':
                self._drop_from_inventory(cmd.obj)

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
        clear_terminal()
        title = [
            "#########################################################################################################",
            "#                       _____ _                                   _                                     #",
            "#                      /__   \ |__   ___    /\/\   __ _ _ __  ___(_) ___  _ __                          #",
            "#                        / /\/ '_ \ / _ \  /    \ / _` | '_ \/ __| |/ _ \| '_ \                         #",
            "#                       / /  | | | |  __/ / /\/\ \ (_| | | | \__ \ | (_) | | | |                        #",
            "#                       \/   |_| |_|\___| \/    \/\__,_|_| |_|___/_|\___/|_| |_|                        #",
            "#                                                                                                       #",
            "#########################################################################################################"
        ]

        for lines in title:
            print(lines)

        time.sleep(1)

        print("")

        prompt_width = 90
        text_width = 80
        text_main = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        text_secondary = "Good Luck..."

        new_text = split_input(text_main, 110)
        animate_text(new_text, 0.02)

        time.sleep(2)

        print("\n")

        new_secondary = split_input(text_secondary, 110)
        animate_text(new_secondary, 0.25)

        time.sleep(2)

        #for i, letter in enumerate(text_main):
        #    sys.stdout.write(letter)
        #    time.sleep(0.02)
        #    if i % 80 == 0 and i != 0:
        #        sys.stdout.write("\n")
        #
        #time.sleep(1)
        #print("\n")
        #for i, letter in enumerate(text_secondary):
        #    sys.stdout.write(letter)
        #    time.sleep(.25)
        #    if i == 80:
        #        sys.stdout.write("\n")
        #
        #time.sleep(2)
        #clear_terminal()
        #return

    def play(self):

        cmd = Input_Parser()

        self.main_player.current_room = self.json_Mansion["First Floor Foyer"]

        #########################################
        # Main Loop
        #########################################
        #self.beginning_text()
        while True:
            #clear_terminal()
            if self.last_command == "move" or self.last_command == "look" or self.last_command == "":
                self._render_room()
            print("")
            cmd.get_input()
            self._process_cmd(cmd)
