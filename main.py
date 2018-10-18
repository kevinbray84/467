from Mansion_Proto.room_sets import *
from Mansion_Proto.player import *
from Mansion_Proto.item_sets import *
from Input_Parser.input_parser import *


################################
#           MAIN CODE          #
################################
main_player = Player()
cmd = Input_Parser()


current_room = foyer


def process_cmd(cmd):
    if cmd.num_commands == 1:
        if cmd.command == 'exit':
            exit()
        elif cmd.command == 'savegame':
            print "Saving game..."
        elif cmd.command == 'loadgame':
            print "Loading game..."

    elif cmd.num_directions == 1:
        main_player.move(cmd.direction)

    elif cmd.num_room_names == 1:
        main_player.move_to(cmd.room_name)

    elif cmd.num_verbs == 1:
        if cmd.verb == 'look':
            # TODO: Implmenet:
            # look_at(parser.obj)   # should display info about  the thing being looked at
            print 'LOOKING at %s' % cmd.obj
        elif cmd.verb == 'take' or cmd.verb == 'get' or cmd.verb == 'grab' or cmd.verb == 'pick up':
            # TODO: Implement:
            # get(parser.obj)    # should add the object to the player's inventory
            print 'GETTING %s' % cmd.obj
        elif cmd.verb == 'put' or cmd.verb == 'use':
            # TODO: Implement:
            # get(parser.obj)    # should use the object if it's in the inventory
            print 'Using %s' % cmd.obj


while True:
    main_player.current_room.get_details()
    cmd.get_input()
    process_cmd(cmd)
