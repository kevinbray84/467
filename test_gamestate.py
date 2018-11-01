from player import *
from GameState import *
from Input_Parser.input_parser import *

def test_look_at():
    print("\ntest 1: trying to look at mail while in First Floor Foyer \n")
    game = GameState()
    action = Input_Parser()
    action.obj = 'mail'

    game._look_at(action)
    print("\ntest 1 complete")


test_look_at()

