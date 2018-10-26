import json
#import roomclass
#import gameclass
from room import *


# parse data into room dictionary object
def inputData(filename):
    with open('rooms/' + filename) as infile:
        Room_dict = json.loads(infile.read())
    return Room_dict


def newgGameStart(gameState):
    room_names = ["diningroom.json", "familyroom.json", "firstfloorfoyer.json", "garage.json", "grandroom.json",
                  "library.json", "mastersuite.json", "panicroom.json", "sarahsroom.json", "secondfloorfoyer.json",
                  "study.json", "veranda.json", "basement.json", "winecellar.json", "secretroom.json"]
    for name in room_names:
        room_dict = inputData(name)
        new_room = Room(room_dict['location'], room_dict['long description'], room_dict['short description'], room_dict['look at'], room_dict['exits'])

        gameState.json_Mansion[room_dict['location']] = new_room
