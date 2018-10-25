from room import Room
from item_sets import *
from feature_sets import *

################################
#       INITIALIZE ROOMS       #
################################

# First Floor
foyer = Room("Foyer")
central = Room("Central staircase")
library = Room("Library")
southern_patio = Room("Southern Patio")
northern_patio = Room("Northern Patio")
master_suite = Room("Master Suite")
veranda_left = Room("Veranda Left")
veranda_middle = Room("Veranda Middle")
veranda_right = Room("Veranda Right")
grand = Room("Grand Room")
family = Room("Family Room")
garage = Room("Garage")
dining = Room("Dining Room")
secret_stairwell = Room("Secret Library Storage Room", True)
pantry = Room("Pantry")
stairwell = Room("Stairwell")

# Second Floor
foyer_second = Room("Second floor foyer")
loft = Room("Loft")
bedroom_second = Room("Bedroom on the second floor")

# Basement
speakeasy = Room("Speakeasy")
panic_room = Room("Panic Room")
unknown_room = Room("Unknown Room")

################################
#           ROOM SETUP         #
################################

###############
# FIRST FLOOR #
###############

# FOYER
foyer.link_room(central, "north")
foyer.link_room(library, "west")
foyer.link_room(dining, "east")

foyer.set_description('You are standing in the Foyer of the mansion. The interior seems to sparkle, and you marvel at the grandeur\n of the entrance with its marble floors and dark mahogany woodwork. In front of you, to the north, is a grand \nstaircase leading to the second floor. Peering into the room to the west, you see books that line the walls \nfrom the floor to the ceiling. You make a mental note that this is the location of the library. To the east \nyou can see what appears to be the dining room with an elongated table adorned with expensive china and fancy \nglassware. In the Foyer, next to the door you see a stack of mail and on the wall hang a set of keys.')

foyer.add_feature("mailbox", mailbox)
# foyer.add_feature("keys", foyer_keys)
foyer.add_item(
    Item("keys", "Some keys...", False))

# CENTRAL
central.link_room(grand, "north")
central.link_room(foyer, "south")
central.link_room(master_suite, "west")
central.link_room(family, "east")
central.link_room(foyer_second, "upstairs")

# LIBRARY
library.link_room(secret_stairwell, "north")
library.link_room(southern_patio, "west")
library.link_room(foyer, "east")

# SECRET STAIRWELL
secret_stairwell.link_room(library, "upstairs")
secret_stairwell.link_room(panic_room, "downstairs")

# SOUTHERN PATIO
southern_patio.link_room(northern_patio, "north")
southern_patio.link_room(library, "east")

# NORTHERN PATIO
northern_patio.link_room(southern_patio, "south")
northern_patio.link_room(master_suite, "east")

# MASTER SUITE
master_suite.link_room(veranda_left, "north")
master_suite.link_room(northern_patio, "west")
master_suite.link_room(central, "east")
master_suite.add_item(Item("passphrase", "A secure passphrase...", False))

# VERANDA LEFT
veranda_left.link_room(master_suite, "south")
veranda_left.link_room(veranda_middle, "east")

# VERANDA MIDDLE
veranda_middle.link_room(grand, "south")
veranda_middle.link_room(veranda_left, "west")
veranda_middle.link_room(veranda_right, "east")

# VERANDA RIGHT
veranda_right.link_room(family, "south")
veranda_right.link_room(veranda_middle, "west")
veranda_right.link_room(stairwell, "east")

# GRAND ROOM
grand.link_room(veranda_middle, "north")
grand.link_room(central, "south")
grand.link_room(family, "east")

# FAMILY ROOM
family.link_room(veranda_right, "north")
family.link_room(garage, "south")
family.link_room(central, "west")
# not getable until jacket is examined
family.add_item(Item("safe combination", "A cryptic code...", False))

# GARAGE
garage.link_room(family, "north")
garage.link_room(dining, "west")
# not getable until BMW trunk is opened
garage.add_item(Item("bolt cutters", "Big sharp bolt cutters...", False))


# DINING ROOM
dining.link_room(pantry, "north")
dining.link_room(foyer, "west")
dining.link_room(garage, "east")
dining.add_item(Item("flashlight", "A bright flashlight...", True))
dining.add_item(Item("silver key", "A key that is silver...", True))

dining.set_description("The dining room has a very lavish feel to it. The table is arranged with only the very best china and cutlery. \nOn the edge of the table you spot a serving tray. Glancing around the rest of the room, you spot something yellow \nsitting on the side table. At the eastern wall you see a door leading out to the Garage. To the north, the \nadjacent room seems to be the Family Room.")
dining.add_feature("food tray", food_tray)
dining.add_feature("side table", side_table)

################
# SECOND FLOOR #
################

# FOYER SECOND  FLOOR
foyer_second.link_room(loft, "west")
foyer_second.link_room(bedroom_second, "east")
foyer_second.link_room(central, "downstairs")
# not getable until you look in the drawers
foyer_second.add_item(Item("engraved key", "A key that's engraved...", False))

# LOFT
loft.link_room(foyer_second, "east")

# BEDROOM
bedroom_second.link_room(foyer_second, "west")
bedroom_second.add_item(Item("diary key", "A key that's engraved...", True))

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
