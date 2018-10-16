from room_sets import *
from player import *
from item_sets import *


################################
#           MAIN CODE          #
################################
main_player = Player()

current_room = foyer

while True:
    main_player.current_room.get_details()
    # command = (input("\nWhat would you like to do?\n> ")).lower()
    command = (input("\nWhere to?\n> ")).lower()

    if command in ["north", "south", "east", "west"]:
        main_player.move(command)

    if command == "explore":
        main_player.current_room.explore()

    if command == "exit":
        exit()

    else:
        print("Not a valid command")
