# 467
Capstone Design Project for Oregon State University Computer Science Post-Bacc Program

1) Place a copy of this zip file in your working directory on flip
2) From you flip working directly, unzip the file using
    > unzip cepheus.zip
3) Change directories to the cepheus directory
    > cd cepheus
4) Run the game by executing the main python program
    > python2 main.py

Interactions and Controls

The text parser should make moving around and interacting with the environment as simple as possible.  Below are some basic commands to be aware of

Game Management
loadgame - load a savegame file from disk
savegame - save your current progress to disk
exit - exit your game without saving
look - re-display the current room’s information
We felt it would be more helpful to the player if the response of the look command re-displayed the current room’s information as it currently exists, rather than the long form description of the room that is reserved for when the player first enters a room and before they take any actions. We emailed Professor Brewster  for confirmation and he said he would allow our definition change.

Movement
go <direction> - move in a given direction (north, south, east, west)
go <exit> - go through an exit described in the room text
go <room name> - go to the indicated room
<exit name> - move to the room connected through the exit
<direction> move in a given direction (north, south, east, west)

Inventory
get / take / grab / pick up <item> - add the requested item to your inventory
drop <item> - drop the item from your inventory into the current room
inventory - displays all items in the player’s inventory
Exploration
look at <object> - display  some more detailed information about an object
Interactions
unlock <object> - attempt to unlock an object
try <object> - attempt to use an object
move <object> - attempt to move an object
enter code - attempt to enter a code into a terminal
use <object> - attempt to use something 
try on <object> - attempt to wear an object
open <object> - attempt to open an object
activate <object> - attempt to activate an object
cut <object> - attempt to cut something
read <object> - read the specified object
watch <object> - watch the specified  object
talk to <character> - talk to a character
rescue <character> - save the specified character
turn on <item name>  - turn on specified item

How to Win
Follow the text described below:
In the First Floor Foyer: 
look at stack of mail
get keys 
go east (to Dining Room)
go east (to Garage)
In the Garage:
 use keys to unlock BMW
 get bolt cutters from trunk
go west (to Dining Room)
In the Dining Room: 
look at food tray
 get silver key
look at side table
 take flashlight 
go north (to Family Room)
In the Family Room:
 look at the couch
 try on the jacket
get safe combination from pocket 
go west (to Master Suite)
In the Master Suite: 
look at portrait
move the portrait
look at safe combination
enter code
 type 12-03-18 (dashes included)
get passphrase 
go south (to Library)
go east (to First Floor Foyer)
go north (to Second Floor Foyer)
In Second Floor Foyer:
look at table
open the drawers
get engraved key
go west (to Sarah’s Room)
In Sarah’s bedroom: 
look under bed
 get diary key
look at side table
read diary (to reveal location of the panic room and how to access it) 
go east (to Second Floor Foyer)
go south (to First Floor Foyer)
go west (to Library)
In Library: 
look at desk
use engraved key in slot (to reveal panic room behind bookshelf)
look at passphrase
use keypad
Type NOPLACELIKEHOME (in capital letters)
Type yes when asked if you would like to enter now
In panic room:
 watch video monitor playback (and notice the mayor taking a tray of food into the wine cellar and opening a door disguised as a back wall) 
go east (to Library) 
go north (to Master Suite)
go east (to Family Room)
go east (to Basement)
In the Basement:
 use flashlight (to reveal the wine cellar)
 use command look
look at trunk
go south (to Wine Cellar)
In the Wine Cellar:
 look at bare wall
 turn on flashlight (to find find the disguised wall from the video)
 use silver key (to open hidden door) 
Type yes when asked if you would like to enter now
In secret room:
 talk to sarah
 use bolt cutters (to cut the chains which bind Sarah) 
 rescue sarah 
YOU WIN!
