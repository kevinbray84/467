class Input_Parser:
    def __init__(self):
        self.input = ''

        self.num_commands = 0
        self.command = ''

        self.num_directions = 0
        self.direction = ''

        self.num_room_names = 0
        self.room_name = ''

        self.num_preps = 0
        self.prep = ''

        self.num_verbs = 0
        self.verb = ''

        self.num_objs = 0
        self.obj = ''
        self.obj_of_prep = ''

        self.commands = ['savegame', 'loadgame']
        self.directions = ['north', 'south', 'east', 'west']
        self.room_names = ['cellar', 'dungeon']
        self.preps = ['in', 'on']
        self.verbs = ['go', 'take', 'drop', 'get', 'put']
        self.objects = ['candle', 'key', 'map', 'chest']

    def _find_command(self):
        words = self.input.split()
        for word in words:
            if word in self.commands:
                self.num_commands += 1
                self.command = word

    def _find_direction(self):
        words = self.input.split()
        for word in words:
            if word in self.directions:
                self.num_directions += 1
                self.direction = word

    def _find_room_name(self):
        words = self.input.split()
        for word in words:
            if word in self.room_names:
                self.num_room_names += 1
                self.room_name = word

    def _find_verb(self):
        words = self.input.split()
        for word in words:
            if word in self.verbs:
                self.num_verbs += 1
                self.verb = word

    def _find_prep(self):
        words = self.input.split()
        for word in words:
            if word in self.preps:
                self.num_preps += 1
                self.prep = word

    def _find_object(self):
        words = self.input.split()
        words.reverse()
        for word in words:
            if word in self.objects:
                self.num_objs += 1
                self.obj = word

    def _find_object_of_prep(self):
        words = self.input.split()
        for word in words:
            if word in self.objects and word != self.obj:
                self.obj_of_prep = word

    def _check_errors(self):
        if self.num_directions + self.num_commands + self.num_room_names > 1:
            print 'You entered too many commands at once'
            self.get_input()

        if self.num_directions == 0 and self.num_commands == 0 and self.num_room_names == 0:
            if self.num_verbs == 0:
                print "I can't tell what you're trying to do.  Maybe use a verb?"
                self.get_input()
            elif self.num_verbs > 1:
                print "You're trying to do too many things at once.  Maybe you have more than one verb?"
                self.get_input()
            elif self.num_objs == 0:
                print "I can't tell what you're trying to interact with.  Maybe you forgot to mention an object?"
                self.get_input()
            elif self.num_preps == 0 and self.num_objs > 1:
                print "You're trying to interact with too many objects at once"
                self.get_input()
            elif self.num_preps > 0 and self.num_objs < 2:
                print "You need two objects if you're going to use a preposition"
                self.get_input()
            elif self.num_objs > 2:
                print "You're trying to interact with WAY too many objects at once"
                self.get_input()
            elif self.num_preps > 1:
                print "You're using a lot of prepositions..."
                self.get_input()

    def get_input(self):
        self.__init__()
        self.input = raw_input("Enter command> ")
        self.input = self.input.lower()
        self._process_input()

    def _process_input(self):
        self._find_command()
        self._find_direction()
        self._find_room_name()
        self._find_prep()
        self._find_verb()
        self._find_object()
        if self.num_preps == 1:
            self._find_object_of_prep()
        self._check_errors()


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
