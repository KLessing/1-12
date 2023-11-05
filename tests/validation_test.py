import pytest

from utils import validate_selection

MOVE_VALIDATION_TEST_CASES = [
    # First Move Tests
    ([6, 1, 4, 3, 5, 2], {}, {7}),
    ([6, 1, 4, 3, 6, 1], {}, {7}),
    ([6, 6, 4, 3, 1, 1], {}, {7}),
    ([6, 6, 1, 1, 6, 1], {}, {7}),
    ([6, 1, 4, 3], {}, {7}),
    ([5, 3, 6, 2], {}, {8}),
    ([6, 6, 6, 6, 6, 6], {}, {6, 12}),
    ([6, 6, 6, 6, 6], {}, {6}),
    ([6, 6, 6, 6], {}, {6, 12}),
    ([6, 6, 6], {}, {6}),
    ([6, 6,], {}, {6, 12}),

    # Empty Result Tests
    ([1, 2], {}, set()),
    ([1, 2, 1], {}, set()),
    ([1, 2, 1, 1, 1, 1], {}, set()),
    ([6, 6, 6, 1, 4, 3], {}, set()),
    ([6, 6, 6, 1], {}, set()),

    # Continued Move Tests
    ([4], {8}, set()),
    ([4], {8, 4}, {4}),
    ([1], {2}, set()),
    ([5, 6], {6}, set()),
    ([6], {6}, {6}),
    ([6], {12, 6}, {6}),
    ([6, 6], {12, 6}, {12, 6}),
    ([5, 5], {10, 5}, {10, 5}),
    ([6, 4, 5, 5], {10, 5}, {10}),
    ([6, 4], {10, 5}, {10}),
    ([4, 4], {8, 4}, {8, 4}),
    ([4, 4], {8}, {8}),

    # Selection of different combinations (when one combination is double dice)
    ([6, 4, 5, 5], {}, {10}),
    ([4, 4, 6, 2], {}, {8}),
    ([5, 5, 6, 4], {}, {10}),
    ([5, 4, 5, 6], {}, {10}),
    ([6, 6, 6, 1], {7}, set()),
]

@pytest.mark.parametrize("new_selection, prev_selection, result", MOVE_VALIDATION_TEST_CASES)
def test_move_validations(new_selection: [int], prev_selection: set(), result: set()):
    assert validate_selection(new_selection, prev_selection, set()) == result
# The already fully completed collection is not tested yet
