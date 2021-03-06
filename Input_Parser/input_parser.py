class Input_Parser:
    def __init__(self):
        self.input = ''

        # initialize words found
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

        # create lists of each type of word
        self.commands = [' savegame ', ' loadgame ',
                         ' exit ', ' inventory ', ' help ', ' look ']
        self.directions = [' north ', ' south ', ' east ',
                           ' west ']
        self.room_names = [' first floor foyer ', ' library ',
                           ' dining room ',  ' panic room ', ' master suite ',
                           ' family room ', ' grand room ', ' veranda ',
                           ' second floor foyer ', ' sarahs room ', ' study ',
                           ' basement ', ' wine cellar ',
                           ' secret room ', ' garage ']
        self.preps = [' in ', ' on ']
        self.verbs = [' grab ', ' get ', ' take ', ' pick up ',
                      ' drop ',
                      ' go ',
                      ' look at ',
                      ' look under ',
                      ' unlock ',
                      ' try on ',
                      ' move ',
                      ' open ',
                      ' read ',
                      ' enter ',
                      ' watch ',
                      ' turn on ',
                      ' use ',
                      ' activate ',
                      ' cut ',
                      ' rescue ',
                      ' talk to '
                      ]
        self.objects = [' key ', ' keys ', ' key peg ',
                        ' keyholder ', ' key holder ', ' key holder on wall ', ' key holders ', ' key pegs ', ' pegs',
                        ' mail ', ' stack ', 'stack of mail ',
                        ' mailbox ',
                        ' silver key ',
                        ' diary key ',
                        ' engraved key ',
                        ' car key ', ' car keys ',
                        ' desk ',
                        ' slot ',
                        ' keypad ',
                        ' statue ',
                        ' corner ',
                        ' food tray ', ' tray ', ' food ', ' foodtray ',
                        ' side table ', ' sidetable ', ' table ',
                        ' desk ', ' tome ', ' large tome ',
                        ' sculpture ',
                        ' back table ',
                        ' flashlight ',
                        ' bmw ', ' car ', ' bmw car ',
                        ' bolt cutters ',
                        ' truck ', ' pickup ',
                        ' portrait ', ' family portrait ', ' family picture ', ' picture ',
                        ' family ',
                        ' combination ', ' safe combination ', ' code ',
                        ' safe ', ' hidden safe ', ' combination ',
                        ' end table ', ' endtable ', ' small crystal containers ', ' small crystal container ',
                        ' crystal container ', ' crystal containers ',
                        ' passcode ',
                        ' end table ',
                        ' fireplace ', ' fire ', ' fire place ', ' ashes ',
                        ' wine bottle ', ' wine ',  ' bottle ', ' wine rack ', ' rack ', ' wine racks ', ' racks ',
                        ' wine receipt ', ' receipt ',
                        ' jacket ', ' suit ', ' suit jacket ',
                        ' sofa ', ' couch ',
                        ' billiards table ', ' pool table ', ' pooltable ',
                        ' patio table ', ' padio table ', ' patiotable ', ' patio ',
                        ' sky ', ' storm ', ' summer storm ', ' clouds ', ' storm in the sky ',
                        ' pocket ',
                        ' piece of paper ', ' paper ',
                        ' newspaper ', ' headline ', ' table with drawers ', ' table top ',
                        ' drawers ', ' drawer ',
                        ' diary ', ' sarah\'s diary ', ' sarahs diary ',
                        ' bed ', ' floor ',
                        ' computer ', ' desktop ', ' computer monitor ', ' laptop ',
                        ' letter ',
                        ' food ', ' canned food ', ' canned goods ', ' water ',
                        ' bottled water ', 'bottled waters ',
                        ' camera ', ' video ', ' video playback ', ' video monitors ',  ' video monitor ',
                        ' monitors ', ' monitor ',
                        ' sarah ', ' daughter ', ' her ',
                        ' chains ', ' chain ', ' chain lock ', ' shackle ',
                        ' passphrase ',
                        ' trunk ', ' large trunk ',
                        ' footprints ', ' foot prints ', ' footprint ', ' foot print ', ' ground ', ' dust ',
                        ' wall ', ' eastern wall ', ' bare wall ', ' back wall ',
                        ' panic room ', ' panic door ', ' keypad ', ' panicroom ',
                        ' grand marble staircase ', ' grand marble stair case ', ' marble staircase ', ' marble stair case ', ' staircase ', ' stair case ',
                        ' oak double doors ', ' double doors ', ' doors ', ' oak doors ',
                        ' pillared entryway ', ' pillared entry way ', ' entryway ', ' entry way ', ' pillar entryway ', ' pillar entry way ', ' pillared ', ' pillar ',
                        ' heavy wooden door ', ' heavy door ', ' wooden door ', ' door ',
                        ' carpeted step ', ' step ', ' carpet ', ' carpeted steps ', ' steps ',
                        ' elegant wooden double french doors ', ' wooden double french doors ', ' double french doors ', ' french doors ', ' doors ',
                        ' elegant double french doors ', ' elegant wooden doors ', ' elegant french doors ', ' wooden french doors ',
                        ' dimly lit staircase ', ' dimly lit stair case ', ' staircase ', ' stair case ', ' stairs ', ' dimly lit stairs ',
                        ' intricately carved mahogany door ', ' carved mahogany door ', ' mahogany door ', ' door ', ' carved door ', ' intricately carved door ',
                        ' massive steel door ', ' massive door ', ' steel door ',
                        ' sliding glass door ', ' glass door ', ' sliding door ',
                        ' disguised hidden stone door ', ' hidden stone door ', ' stone door ', ' disguised stone door ', ' disguised door ', ' hidden door ',
                        ' opaque glass door ', ' opaque door ',
                        ' decorated door ', ' picture door ', ' decorative door ', ' door with pictures ',
                        ' oaken panel door ', ' oaken door ', ' panel door ', ' oak door ', ' oak panel door ', ' solid oak door ', ' solid door ',
                        ' rosewood sliding door ', ' rosewood door ',
                        ' upstairs ', ' downstairs '
                        ]

    """
    The following functions find the specified word type in the input and store
    them in this object's member variables
    """

    def _find_command(self):
        if 'look at' in self.input or 'look under' in self.input:
            return self
        for word in self.commands:
            if word in self.input:
                if len(word) > len(self.command):  # only get longest matching word
                    if len(self.command) == 0:     # dont double count long match
                        self.num_commands += 1
                self.command = word.strip()

    def _find_direction(self):
        for word in self.directions:
            if word in self.input:
                self.num_directions += 1
                self.direction = word.strip()

    def _find_room_name(self):
        for word in self.room_names:
            if word in self.input:
                if len(word) > len(self.room_name):  # only get longest matching word
                    if len(self.room_name) == 0:     # dont double count long match
                        self.num_room_names += 1
                    self.room_name = word.strip()

    def _find_verb(self):
        for word in self.verbs:
            if word in self.input:
                if len(word) > len(self.verb):  # only get longest matching word
                    if len(self.verb) == 0:     # dont double count long match
                        self.num_verbs += 1
                    self.verb = word.strip()

    def _find_prep(self):
        for word in self.preps:
            if word in self.input and self.verb != 'turn on' and self.verb != 'try on':  # need special case for turn on
                self.num_preps += 1
                self.prep = word.strip()

    def _find_object(self):
        loc = len(self.input)
        if self.num_preps == 1:
            loc = self.input.find(self.prep)
        for word in self.objects:
            if word in self.input[0:loc]:
                # print '%d: found %s in %s' % (
                #    self.num_objs, word, self.input[0:loc])
                if len(word) > len(self.obj):  # only get longest matching word
                    if len(self.obj) == 0:     # dont double count long match
                        self.num_objs += 1
                    self.obj = word.strip()

    def _find_object_of_prep(self):
        loc = len(self.input)
        if self.num_preps == 1:
            loc = self.input.find(self.prep)
        for word in self.objects:
            if word in self.input[loc:len(self.input)]:
                if len(word) > len(self.obj_of_prep):  # only get longest matching word
                    if len(self.obj_of_prep) == 0:     # dont double count long match
                        self.num_objs += 1
                    self.obj_of_prep = word.strip()

    """
    This function checks for any errors in the input
    """

    def _check_errors(self):
        if self.num_directions + self.num_commands + self.num_room_names > 1:
            print 'You entered too many commands at once'
            self.get_input()

        if self.num_directions == 0 and self.num_commands == 0 and self.num_room_names == 0:
        #    if self.num_verbs == 0:
            #    print "I can't tell what you're trying to do.  Maybe use a verb?"
            #    self.get_input()
            if self.num_verbs > 1:
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

    """
    This function collects input text from the user
    """

    def get_input(self):
        self.__init__()
        self.input = raw_input("Enter command> ")
        self.input = ' ' + self.input.lower() + ' '
        print '\n'
        self._process_input()

    """
    This function calls the required functions to parse the input
    """

    def _process_input(self):
        self._find_command()
        self._find_direction()
        self._find_room_name()
        self._find_verb()
        self._find_prep()
        self._find_object()
        if self.num_preps == 1:
            self._find_object_of_prep()
        self._check_errors()
