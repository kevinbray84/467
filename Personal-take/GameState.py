from player import Player
from room_sets import *
from item_sets import *

class GameState:
    def __init__(self):
        self.main_player = Player()
        self.mansion = {}
        self.game_items = {}
        self.current_room = None

    def build_item_sets(self):
        self.game_items["keys"] = Item("keys", "Rusty golden key, looks like it could open anything.")

    def build_mansion(self):

        self.mansion["foyer"] = Room("Foyer")
        self.mansion["central"] = Room("Central staircase")
        self.mansion["library"] = Room("Library")
        self.mansion["southern_patio"] = Room("Southern Patio")
        self.mansion["northern_patio"] = Room("Northern Patio")
        self.mansion["master_suite"] = Room("Master Suite")
        self.mansion["veranda_left"] = Room("Veranda Left")
        self.mansion["veranda_middle"] = Room("Veranda Middle")
        self.mansion["veranda_right"] = Room("Veranda Right")
        self.mansion["grand"] = Room("Grand Room")
        self.mansion["family"] = Room("Family Room")
        self.mansion["garage"] = Room("Garage")
        self.mansion["dining"] = Room("Dining Room")
        self.mansion["secret_stairwell"] = Room("Secret Library Storage Room", True)
        self.mansion["pantry"] = Room("Pantry")
        self.mansion["stairwell"] = Room("Stairwell")

        # Second Floor
        self.mansion["foyer_second"] = Room("Second floor foyer")
        self.mansion["loft"] = Room("Loft")
        self.mansion["bedroom_second"] = Room("Bedroom on the second floor")

        # Basement
        self.mansion["speakeasy"] = Room("Speakeasy")
        self.mansion["panic_room"] = Room("Panic Room")
        self.mansion["unknown_room"] = Room("Unknown Room")


        ################################
        #           ROOM SETUP         #
        ################################

        ###############
        # FIRST FLOOR #
        ###############

        # FOYER
        self.mansion["foyer"].link_room(central, "north")
        self.mansion["foyer"].link_room(library, "west")
        self.mansion["foyer"].link_room(dining, "east")

        self.mansion["foyer"].set_description('You are standing in the Foyer of the mansion. The interior seems to sparkle, and you marvel at the grandeur\n of the entrance with its marble floors and dark mahogany woodwork. In front of you, to the north, is a grand \nstaircase leading to the second floor. Peering into the room to the west, you see books that line the walls \nfrom the floor to the ceiling. You make a mental note that this is the location of the library. To the east \nyou can see what appears to be the dining room with an elongated table adorned with expensive china and fancy \nglassware. In the Foyer, next to the door you see a stack of mail and on the wall hang a set of keys.')

        self.mansion["foyer"].add_feature("mailbox", mailbox)
        self.mansion["foyer"].add_feature("keys", foyer_keys)

        # CENTRAL
        self.mansion["central"].link_room(grand, "north")
        self.mansion["central"].link_room(foyer, "south")
        self.mansion["central"].link_room(master_suite, "west")
        self.mansion["central"].link_room(family, "east")
        self.mansion["central"].link_room(foyer_second, "upstairs")

        # LIBRARY
        self.mansion["library"].link_room(secret_stairwell, "north")
        self.mansion["library"].link_room(southern_patio, "west")
        self.mansion["library"].link_room(foyer, "east")

        # SECRET STAIRWELL
        self.mansion["secret_stairwell"].link_room(library, "upstairs")
        self.mansion["secret_stairwell"].link_room(panic_room, "downstairs")

        # SOUTHERN PATIO
        self.mansion["southern_patio"].link_room(northern_patio, "north")
        self.mansion["southern_patio"].link_room(library, "east")

        # NORTHERN PATIO
        self.mansion["northern_patio"].link_room(southern_patio, "south")
        self.mansion["northern_patio"].link_room(master_suite, "east")

        # MASTER SUITE
        self.mansion["master_suite"].link_room(veranda_left, "north")
        self.mansion["master_suite"].link_room(northern_patio, "west")
        self.mansion["master_suite"].link_room(central, "east")

        # VERANDA LEFT
        self.mansion["veranda_left"].link_room(master_suite, "south")
        self.mansion["veranda_left"].link_room(veranda_middle, "east")

        # VERANDA MIDDLE
        self.mansion["veranda_middle"].link_room(grand, "south")
        self.mansion["veranda_middle"].link_room(veranda_left, "west")
        self.mansion["veranda_middle"].link_room(veranda_right, "east")

        # VERANDA RIGHT
        self.mansion["veranda_right"].link_room(family, "south")
        self.mansion["veranda_right"].link_room(veranda_middle, "west")
        self.mansion["veranda_right"].link_room(stairwell, "east")

        # GRAND ROOM
        self.mansion["grand"].link_room(veranda_middle, "north")
        self.mansion["grand"].link_room(central, "south")
        self.mansion["grand"].link_room(family, "east")

        # FAMILY ROOM
        self.mansion["family"].link_room(veranda_right, "north")
        self.mansion["family"].link_room(garage, "south")
        self.mansion["family"].link_room(central, "west")

        # GARAGE
        self.mansion["garage"].link_room(family, "north")
        self.mansion["garage"].link_room(dining, "west")

        # DINING ROOM
        self.mansion["dining"].link_room(pantry, "north")
        self.mansion["dining"].link_room(foyer, "west")
        self.mansion["dining"].link_room(garage, "east")

        self.mansion["dining"].set_description("The dining room has a very lavish feel to it. The table is arranged with only the very best china and cutlery. \nOn the edge of the table you spot a serving tray. Glancing around the rest of the room, you spot something yellow \nsitting on the side table. At the eastern wall you see a door leading out to the Garage. To the north, the \nadjacent room seems to be the Family Room.")
        self.mansion["dining"].add_feature("food tray", food_tray)
        self.mansion["dining"].add_feature("side table", side_table)

        ################
        # SECOND FLOOR #
        ################

        # FOYER SECOND  FLOOR
        foyer_second.link_room(loft, "west")
        foyer_second.link_room(bedroom_second, "east")
        foyer_second.link_room(central, "downstairs")

        # LOFT
        loft.link_room(foyer_second, "east")

        # BEDROOM
        bedroom_second.link_room(foyer_second, "west")

        #################
        #   BASEMENT    #
        #################
        stairwell.link_room(veranda_right, "west")
        stairwell.link_room(speakeasy, "south")

        speakeasy.link_room(stairwell, "north")
        speakeasy.link_room(unknown_room, "east")
        speakeasy.link_room(panic_room, "south")

        panic_room.link_room(speakeasy, "north")
        panic_room.link_room(secret_stairwell, "stairwell")

        self.current_room = self.mansion["foyer"]

    def move(self, direction):
        if direction in self.current_room.linked_rooms:
            self.current_room = self.current_room.linked_rooms[direction]
        else:
            print("You can't go that way")
            return self

    def foyer_action_check(self, verb, noun):
        return

    def play(self):
        print(self.current_room.get_details())

        while True:

            # command = (input("\nWhat would you like to do?\n> ")).lower()
            command = (raw_input("\nWhat would you like to do?\n> ")).lower()

            movement = ["go"]
            observation = ["look"]
            pickup = ["take"]

            if len(command.split()) > 1:
                firstWord, rest = command.split(None, 1)
            else:
                firstWord = command
                rest = command

            if rest == "look":
                print(self.current_room.get_description())

            if firstWord in movement:
                self.move(rest)
                self.current_room.get_details()

            elif firstWord in observation:
                if rest in self.current_room.features:
                    curr_feature = self.current_room.features[rest]
                    if curr_feature.hasAction:
                        self.action_check(self.current_room.name, rest)
                    else:
                        print (curr_feature.get_description())

            elif firstWord == "inventory":
                self.check_inventory()

            elif firstWord in pickup:
                if rest in self.current_room.items_in_room:
                    self.current_room.take_item(self.game_items["keys"])
                    self.main_player.take_item(self.game_items["keys"])
                    print("Took " + rest)

            else:
                print("Incorrect response, try again")

            if command == "exit":
                exit()

    def action_check(self, room_name, feature_name):
        if room_name.lower() == "foyer":
            if feature_name == "keys":
                print("Keys are now available in room")
                self.current_room.add_item(keys)

    def check_inventory(self):
        if bool(self.main_player.inventory) == False:
            print("Nothing")
        else:
            for items in self.main_player.inventory:
                print(items.name)







