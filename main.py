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
        main_player.move_to(parser.room_name)

    elif parser.num_verbs == 1:
        if parser.verb == 'look':
            # TODO: Implmenet:
            # look_at(obj)   # should display info about  the thing being looked at
            print 'LOOKING at %s' % parser.obj
        elif parser.verb == 'take' or parser.verb == 'get' or parser.verb == 'grab':
            # TODO: Implement:
            # get(obj)    # should add the object to the player's inventory
            print 'GETTING %s' % parser.obj
        elif parser.verb == 'put' or parser.verb == 'use':
            # TODO: Implement:
            # get(obj)    # should use the object if it's in the inventory
            print 'Using %s' % parser.obj
