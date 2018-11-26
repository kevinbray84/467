from player import *
from GameState import *
import pickle
import glob
import os


################################
#           MAIN CODE          #
################################
game = GameState()

save_game = False
load_game = False
done_game = False

while not done_game:
    while load_game == False and save_game == False and done_game == False:
        save_game, load_game, done_game = game.play()

    if save_game:
        fname = raw_input("    Enter filename> ")
        if not fname.endswith('.sav'):
            fname = fname + ".sav"
        file_handler = open(fname, 'w')
        pickle.dump(game, file_handler)
        print "Game saved!"

        # this should restart the game from the saved point
        file_handler = open(fname, 'r')
        game = pickle.load(file_handler)
        save_game, load_game, done_game = game.play()

    if load_game:
        # save a copy of current so it can be restarted if player changes thier mind
        old_game = game

        print "The following savegames are available"
        for file in os.listdir('.'):
            if file.endswith(".sav"):
                print "    %s" % file

        fname = raw_input("    Enter file name> ")
        try:
            if not fname.endswith(".sav"):
                fname = fname + ".sav"
            file_handler = open(fname, 'r')
        except:
            print "File not found"
            game = old_game
            save_game, load_game, done_game = game.play()
            continue

        print "All unsaved progress will be lost.  Do you really want to load?"
        choice = raw_input("y/n > ")
        if 'y' in choice:
            game = pickle.load(file_handler)
            save_game, load_game, done_game = game.play()
        else:
            game = old_game
            save_game, load_game, done_game = game.play()

        if done_game:
            print "YOU WIN!"
            exit()
