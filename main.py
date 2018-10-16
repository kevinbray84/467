from Mansion_Proto.room_sets import *
from Mansion_Proto.player import *
from Mansion_Proto.item_sets import *
from Input_Parser.input_parser import *


################################
#           MAIN CODE          #
################################
main_player = Player()
parser = Input_Parser()


current_room = foyer

while True:
    main_player.current_room.get_details()
    parser.get_input()

    if parser.num_commands == 1:
        if parser.command == 'exit':
            exit()

    elif parser.num_directions == 1:
        main_player.move(parser.direction)

    elif parser.num_room_names == 1:
        print 'move to %s' % parser.room_name
