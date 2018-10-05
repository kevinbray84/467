input = ['go north', 'take candle', 'drop key', 'get the candle key and map']

verbs = ['go', 'take', 'drop', 'get']
objects = ['candle', 'key', 'map']
directions = ['north', 'south', 'east', 'west']


def find_verb(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in verbs:
            num_found += 1
            # print ('    %d: found %s in verbs' % (num_found, word))
            verb = word
    if num_found == 1:
        print ('    Verb: %s' % verb)
    elif num_found == 0:
        print '    Verb: VERB NOT FOUND'
    elif num_found > 1:
        print '    Verb: TOO MANY VERBS FOUND'


def find_object(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in objects:
            num_found += 1
            obj = word
    if num_found == 1:
        print ('    Object: %s' % obj)
    elif num_found == 0:
        print '    Object: OBJECT NOT FOUND'
    elif num_found > 1:
        print '    Object: TOO MANY OBJECTS FOUND'


def find_direction(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in directions:
            num_found += 1
            direction = word
    if num_found == 1:
        print ('    Direction: %s' % direction)
    elif num_found == 0:
        print '    Direction: DIRECTION NOT FOUND'
    elif num_found > 1:
        print '    Direction: TOO MANY DIRECTIONS FOUND'


for user_input in input:
    print ('INPUT: %s' % user_input)
    find_verb(user_input)
    find_object(user_input)
    find_direction(user_input)
