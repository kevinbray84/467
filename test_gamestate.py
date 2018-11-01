from player import *
from GameState import *
from Input_Parser.input_parser import *

def test_look_at():
    game = GameState()
    action = Input_Parser()
    action.obj = 'mail'

    game._look_at(action)
    print("test 1 complete")


test_look_at()

