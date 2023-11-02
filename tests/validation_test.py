import pytest
from src.game import Game
from src.validator import validate_selection

SCREEN_SIZE = (852, 480)
PLAYER_NAMES = ["Player 1"]
CAPTION = "1 - 12"

game_instance = Game(SCREEN_SIZE, PLAYER_NAMES, CAPTION)

TEST_FIRST_MOVE = [
    ([6, 1, 4, 3, 5, 2], True), # 3 x 7
    ([6, 6, 6, 6, 6, 6] , True), # 6 x 6
    ([6, 6, 6, 6] , True), # 4 x 6
    ([6, 1, 4, 3] , True), # 2 x 7
    ([6, 6, 6, 1, 4, 3] , False), # 2 x 7, 2 x 6
    ([5, 5, 6, 4] , True),# 2 x 5 + 6 + 4 = 2 x 10 TODO
]

# Test first moves with empty score
@pytest.mark.parametrize("test_case, valid", TEST_FIRST_MOVE)
def test_first_move(test_case: [int], valid: bool):
    assert validate_selection(test_case, game_instance.scores[0], True) == valid

def test_second_move():
    game_instance.scores[0].set_selection([6, 6])
    test_values = [6, 6]
    assert validate_selection(test_values, game_instance.scores[0], False) == True

