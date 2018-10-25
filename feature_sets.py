# coding: utf-8

from room_sets import *
from feature import *
from item_sets import *
from types import *
from room import Room


mailbox = Feature("mailbox")
mailbox.set_description("There is a stack of recently delivered mail by the door. After analyzing the \n\“kidnapper’s note\” we determined that the letters used to create it came from the \nmagazines PEOPLE, TIME, and THE NEW YORKER. Is it a coincidence that the Mayor seems to subscribe \nto all three?")

foyer_keys = Feature("keys")
foyer_keys.set_description("Hanging from peg are a set of what appear to be car keys. The logo on the keychain is BMW.")
foyer_keys.has_action()


def add_key_action(self):
    self.add_item(skeleton_key)
    print("Key added to room")


#foyer.action = MethodType(add_key_action, foyer)





food_tray = Feature("food tray")
food_tray.set_description("The food tray has a single empty bowl and a single empty juice box on it. \nLooking inside the bowl you see the remnants of what you can only assume to be is soup.\n Why is there only a single serving of food on the tray? And which family member is drinking \njuice boxes? Something doesn’t seem right. Under the napkin you spot a glint of silver. It \nappears to be a silver key! Now what does this unlock…")

side_table = Feature("side table")
side_table.set_description("You approach the side table and take a closer look at the yellow object \nthat caught your eye. It is a flashlight. This could come in handy later.")



