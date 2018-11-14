from player import *
from GameState import *
import pickle


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
        print "SAVING GAME"
        file_handler = open('test.sav', 'w')
        pickle.dump(game, file_handler)
        print "Game saved, exiting..."
        
        # this should restart the game from the saved point
        file_handler = open('test.sav', 'r')
        game = pickle.load(file_handler)
        save_game, load_game, done_game = game.play()

    if load_game:
        print "LOADING GAME"
        file_handler = open('test.sav', 'r')
        game = pickle.load(file_handler)
        save_game, load_game, done_game = game.play()
