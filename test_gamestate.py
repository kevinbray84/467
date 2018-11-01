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

    print("\ntest 2: trying to look at mailbox while in First Floor Foyer")
    print("should print same response as test 1\n")
    action.obj = 'mailbox'
    game._look_at(action)
    print("\ntest 2 complete")

    print("\ntest 3: trying to look at keys while in First Floor Foyer")
    action.obj = 'keys'
    game._look_at(action)
    print("\ntest 3 complete")

    print("\ntest 4: trying to look at key peg while in First Floor Foyer")
    print("should print same response as test 3\n")
    action.obj = 'key peg'
    game._look_at(action)
    print("\ntest 4 complete")




test_look_at()

