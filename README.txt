To run:
python main.py

This was my attempt at room/game classes and filling the classes with JSON data. I tried to write almost all of the dialog branches into the JSON room files so if the 'PLAYER' were to 
type in <look at mail> while they are in the first floor foyer, then the game engine/verb parser could match that with game1.firstfloorfoyer.lookat['mail'], which holds the 
corresponding response that should print to the screen. The items JSON file will hold the rest of the interaction print outs. I tried to write the JSON files in such a way that
they would only need to utilize a base class. I kept the JSON parameters the same, using: Location, long description, short description, look at, and exits, to separate the data.
If changes needed to be made to fit a sub class structure feel free to let me know as making changes to the formating is easy enough.

I also listed the proper exits to each room in their respective JSON file, which after parsing, can now be accessed as such: game1.roomname.exits['direction'] 
(example:game1.panicRoom.exits['west']) The default is an empty string, so if you are having trouble linking rooms I was thinking that another option could be to parse the 'PLAYER' 
movement command <go north> and check it against whether the corresponding game1.roomname.exits['direction'] is an empty string or not. If it is, then print out "Can't go that way" 
or something. If there is a string, then you could update the players location with the string location and then use that value to start the new room dialog, 
print(game1.newroom.long_description).

I don't know how plausible all that is since my knowledge of python is still severely lacking. In the long run it might be more work versus setting up a room linkage system. 
These are just my first thoughts when I was contemplating how to change rooms. Also as a final note, forgive the poor writing/spelling mistakes on the room data. I figured that 
would be cleaned up as we progress.