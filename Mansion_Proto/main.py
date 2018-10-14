from room_sets import *
from player import *

################################
#           MAIN CODE          #
################################
main_player = Player()

current_room = foyer

while True:
    main_player.current_room.get_details()
    # command = (input("\nWhat would you like to do?\n> ")).lower()
    command = (input("\nWhere to?\n> ")).lower()
    main_player.move(command)
