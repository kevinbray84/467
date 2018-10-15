input = ['go north', 'take candle', 'drop key',
         'get the candle key and map', 'put the map in the chest', 'get on the map']

verbs = ['go', 'take', 'drop', 'get', 'put']
objects = ['candle', 'key', 'map', 'chest']
directions = ['north', 'south', 'east', 'west']
prepositions = ['in', 'on']

# TODO: Change to a single function taht takes 'word_type' to look for


def find_verb(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in verbs:
            num_found += 1
            # print ('    %d: found %s in verbs' % (num_found, word))
            verb = word
    if num_found == 1:
        return (0, verb)
    elif num_found == 0:
        return (-1, 'ERR: verb not found')
    elif num_found > 1:
        return (-2, 'ERR: too many verbs')


def find_object(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in objects:
            num_found += 1
            obj = word
    if num_found == 1:
        return (0, obj)
    elif num_found == 0:
        return (-1, 'ERR: object not found')
    elif num_found > 1:
        return (-2, 'ERR: too many objects found')


def find_direction(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in directions:
            num_found += 1
            direction = word
    if num_found == 1:
        return (0, direction)
    elif num_found == 0:
        return (-1, 'ERR: direction not found')
    elif num_found > 1:
        return (-2, 'ERR: too many directions found')


def find_prep(input):
    num_found = 0
    words = input.split()
    for word in words:
        if word in prepositions:
            num_found += 1
            prep = word
    if num_found == 1:
        return (0, prep)
    elif num_found == 0:
        return (-1, 'ERR: direction not found')
    elif num_found > 1:
        return (-2, 'ERR: too many directions found')


def process_input(input):
    print ('INPUT: %s' % input)
    verb = 'NULL'
    obj = 'NULL'
    prep = 'NULL'
    direction = 'NULL'

    (code, direction) = find_direction(input)
    if code == 0:
        print ("Moving %s" % direction)
    else:
        direction = 'NULL'

    if direction == 'NULL':
        (code, verb) = find_verb(input)
        if code == -1:
            print 'ERR: I can\'t tell what you\'re trying to do'
            verb = 'NULL'
        if code == -2:
            print 'ERR: You\'re trying to do too many things at once'
            verb = 'NULL'

        (code, obj) = find_object(input)
        if code == -1:
            print 'ERR: I can\'t tell what you\'re trying to interact with'
            obj = 'NULL'
        if code == -2:
            print 'ERR: You\'re trying to interact with too many things at once'
            obj = 'NULL'

        (code, prep) = find_prep(input)
        if code == -1:
            prep = 'NULL'
        if code == -2:
            prep = 'NULL'

    command = [verb, obj, prep]
    print command


for user_input in input:
    process_input(user_input)


while True:
    input = raw_input('Enter Command> ')
    process_input(input)
