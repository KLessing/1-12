import pytest
from src.game import Game
from src.validator import validate_selection

SCREEN_SIZE = (852, 480)
PLAYER_NAMES = ["Player 1"]
CAPTION = "1 - 12"

game_instance = Game(SCREEN_SIZE, PLAYER_NAMES, CAPTION)

MOVE_VALIDATION_TEST_CASES = [
    # First Move Tests
    ({}, [6, 1, 4, 3, 5, 2], True), # 3 x 7    
    ({}, [6, 6, 6, 6, 6, 6] , True), # 6 x 6
    ({}, [6, 6, 6, 6] , True), # 4 x 6
    ({}, [6, 1, 4, 3] , True), # 2 x 7
    ({}, [6, 6, 6, 1, 4, 3] , False), # 2 x 7, 2 x 6
    ({}, [5, 3, 6, 2] , True), # 2 x 8
    # Continued Move Tests
    ({1}, [2], False),
    ({6, 6}, [6, 5], False),
    ({6, 6}, [6], True),
    ({6, 6}, [6, 6], True),
    # TODO Keep Combination selection (Gets removed after first single selection)
    ({10, 5}, [5], True),
    ({10, 5}, [5, 5], True),
    ({10, 5}, [6, 4, 5, 5], True),
    ({10, 5}, [6, 4], True),
    # TODO Enable selection of different combinations (when one combination is double dice)
    ({}, [5, 5, 6, 4] , True), # 2 x 5 + 6 + 4 = 2 x 10
    ({}, [4, 4, 6, 2] , True), # 2 x 4 + 6 + 2 = 2 x 8
    ({10}, [5, 5, 6, 4], True),
    ({10}, [5, 4, 5, 6], True),    
]

@pytest.mark.parametrize("score, test_case, valid", MOVE_VALIDATION_TEST_CASES)
def test_move_validations(score: set(), test_case: [int], valid: bool):
    game_instance.scores[0].set_selection(score)
    assert validate_selection(test_case, game_instance.scores[0], len(score) == 0) == valid
