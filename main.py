import gameclass
import roomclass
import dataparse
import json
import input_parser

# create instance of game class
game1 = gameclass.game()
# call newgameStart to populate game instance with corresponding JSON data
dataparse.newgameStart(game1)

# print out game object room data to prove that json data has been
# successfully parsed into game class object
print ("\nlocation: " + game1.panicRoom.location)
print("\nlong description: " + game1.panicRoom.long_description)
print("\nshort description: " + game1.panicRoom.short_description)
print("\nlook at food: " + game1.panicRoom.lookat['food'])
print("\nlook at video: " + game1.panicRoom.lookat['video'])
print("\nexit to north: " + game1.panicRoom.exits['north'])
print("\nexit to east: " + game1.panicRoom.exits['east'])
print("\nexit to south: " + game1.panicRoom.exits['south'])
print("\nexit to west: " + game1.panicRoom.exits['west'])

'''
Print out should match this data
{
    "location": "Panic Room",
    "long description": "You walk through the passcode locked door and find yourself in a room the size of a bedroom. Within the room you see a wall of video surveillance monitors 
		and a stockpile of food and bottled water in the corner. This it the first time you have ever seen a genuine panic room and looking around it looks like a person could hold 
		out for quite some time in here. The only exit is the steel door you came in through on the east wall.",
    "short description": "You are in the Panic Room. There is food in the corner and video monitors on the wall. The only exit is the steel door to the east.",
    "look at":{
        "food":"You approach the food and see that it is a bunch of canned goods and bottled water. This amount should easily last a family enough time for help to arrive.",
        "video":"You approach the video monitors and see that there are cameras throughout the house. Better erase all traces you were here, you think to yourself. As you use the 
			controls to rewind the tapes you notie something odd. The Mayor is seen taking a tray of food down into the basement. Your heartbeat quickens, could this be it? Is she 
			still alive in the house? You follow the Mayor's progress as he decends the stairs into the basement, goes into the wine cellar, and finally approaches a wall. The wall 
			turns out to actually be a door! It is tough to make out with the angle, but it looks like he used some type of key. You must go and search the wine cellar!"
    },
    "exits": {
        "north":"",
        "east":"Library",
        "south":"",
        "west":""
    }
}
'''
