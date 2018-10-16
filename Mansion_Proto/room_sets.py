from room import Room
from item_sets import *

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
secret_stairwell = Room("Secret Library Storage Room")
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

# GARAGE
garage.link_room(family, "north")
garage.link_room(dining, "west")

# DINING ROOM
dining.link_room(pantry, "north")
dining.link_room(foyer, "west")
dining.link_room(garage, "east")

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
