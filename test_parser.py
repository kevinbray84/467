from Input_Parser.input_parser import *

parser = Input_Parser()

while True:
    parser.get_input()

    print ("Found %d command: %s" % (parser.num_commands, parser.command))
    print ("Found %d direction: %s" %
           (parser.num_directions, parser.direction))
    print ("Found %d room names: %s" %
           (parser.num_room_names, parser.room_name))
    print ("Found %d preps: %s" % (parser.num_preps, parser.prep))
    print ("Found %d verbs: %s" % (parser.num_verbs, parser.verb))
    print ("Found %d objects: \n\t object: %s \n\t object of prep: %s" %
           (parser.num_objs, parser.obj, parser.obj_of_prep))
