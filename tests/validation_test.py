from src.game import Game
from src.validator import validate_selection

SCREEN_SIZE = (852, 480)
PLAYER_NAMES = ["Player 1"]
CAPTION = "1 - 12"

game_instance = Game(SCREEN_SIZE, PLAYER_NAMES, CAPTION)

def test_3x7():
    test_values = [6, 1, 4, 3, 5, 2]
    assert validate_selection(test_values, game_instance.scores[0], True) == True

def test_6x6():
    test_values =  [6, 6, 6, 6, 6, 6]
    assert validate_selection(test_values, game_instance.scores[0], True) == True

def test_false():
    test_values =  [6, 6, 6, 1, 4, 3]
    assert validate_selection(test_values, game_instance.scores[0], True) == False    

def test_second_move():
    game_instance.scores[0].set_selection([6, 6])
    test_values = [6, 6]
    assert validate_selection(test_values, game_instance.scores[0], False) == True

