from room_sets import *

################################
#           MAIN CODE          #
################################
current_room = foyer

while True:
    current_room.get_details()
    command = (input("\nWhere to?\n> ")).lower()
    current_room = current_room.move(command)
