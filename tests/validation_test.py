from src.game import Game
from src.validator import validate_selection

SCREEN_SIZE = (852, 480)
PLAYER_NAMES = ["Player 1", "Player 2"]
CAPTION = "1 - 12"

game_instance = Game(SCREEN_SIZE, PLAYER_NAMES, CAPTION)

def test_answer():
    test_values = [6, 1, 4, 3, 5, 2]
    assert validate_selection(test_values, game_instance.scores[0], True) == True