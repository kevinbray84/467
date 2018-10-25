import json
import roomclass
import gameclass
from room import *


# parse data into room dictionary object
def inputData(filename):
    with open('rooms/' + filename) as file:
        Room_dict = json.loads(file.read())
    return Room_dict


def newgGameStart(gameState):
    room_names = ["diningroom.json", "familyroom.json", "firstfloorfoyer.json", "garage.json", "grandroom.json",
                  "library.json", "mastersuite.json", "panicroom.json", "sarahsroom.json", "secondfloorfoyer.json",
                  "study.json", "veranda.json", "basement.json", "winecellar.json", "secretroom.json"]
    for name in room_names:
        room_dict = inputData(name)
        new_room = Room(room_dict['location'], room_dict['long description'], room_dict['short description'], room_dict['look at'], room_dict['exits'])

        gameState.json_Mansion[room_dict['location']] = new_room


# poulate rooms with json data to start new game
def newgameStart(gameName):
    name = "diningroom.json"
    new_room_dict = inputData(name)
    gameName.diningRoom.populate(new_room_dict['location'], new_room_dict['long description'],
                                 new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "familyroom.json"
    new_room_dict = inputData(name)
    gameName.familyRoom.populate(new_room_dict['location'], new_room_dict['long description'],
                                 new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "firstfloorfoyer.json"
    new_room_dict = inputData(name)
    gameName.familyRoom.populate(new_room_dict['location'], new_room_dict['long description'],
                                 new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "garage.json"
    new_room_dict = inputData(name)
    gameName.garage.populate(new_room_dict['location'], new_room_dict['long description'],
                             new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "grandroom.json"
    new_room_dict = inputData(name)
    gameName.grandRoom.populate(new_room_dict['location'], new_room_dict['long description'],
                                new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "library.json"
    new_room_dict = inputData(name)
    gameName.library.populate(new_room_dict['location'], new_room_dict['long description'],
                              new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "mastersuite.json"
    new_room_dict = inputData(name)
    gameName.mastersuite.populate(new_room_dict['location'], new_room_dict['long description'],
                                  new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "panicroom.json"
    new_room_dict = inputData(name)
    gameName.panicRoom.populate(new_room_dict['location'], new_room_dict['long description'],
                                new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "sarahsroom.json"
    new_room_dict = inputData(name)
    gameName.sarahsroom.populate(new_room_dict['location'], new_room_dict['long description'],
                                 new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "secondfloorfoyer.json"
    new_room_dict = inputData(name)
    gameName.secondfloorfoyer.populate(new_room_dict['location'], new_room_dict['long description'],
                                       new_room_dict['short description'], new_room_dict['look at'],
                                       new_room_dict['exits'])

    name = "study.json"
    new_room_dict = inputData(name)
    gameName.study.populate(new_room_dict['location'], new_room_dict['long description'],
                            new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "veranda.json"
    new_room_dict = inputData(name)
    gameName.veranda.populate(new_room_dict['location'], new_room_dict['long description'],
                              new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "basement.json"
    new_room_dict = inputData(name)
    gameName.basement.populate(new_room_dict['location'], new_room_dict['long description'],
                               new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "winecellar.json"
    new_room_dict = inputData(name)
    gameName.winecellar.populate(new_room_dict['location'], new_room_dict['long description'],
                                 new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])

    name = "secretroom.json"
    new_room_dict = inputData(name)
    gameName.secretRoom.populate(new_room_dict['location'], new_room_dict['long description'],
                                 new_room_dict['short description'], new_room_dict['look at'], new_room_dict['exits'])
