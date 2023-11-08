from .globals import MAX_DICE_COUNT

# selection = new selection on the field
# selected = already selected combinations from previous move (used dice)
# collected = full collected values
# return valid combinations
def validate_selection(selection: [int], selected: set(), collected: set()):
    combinations = _get_value_combinations(selection)
    combinations = combinations - collected

    # check if already selected values available (not first move)
    if len(selected) > 0:
        # keep only already validated values from new validation
        combinations = combinations.intersection(selected)
        
    return combinations
    
""" Private Functions """

def _validate_uneven_count(values):
    # are all numbers equal? 
    # use set to group values and check length
    if len(set(values)) == 1:
        # return the number
        return {values[0]}
    else:
        return set()

def _valid_special_combinations(values):
    # check individual values for special cases
    count_single_values = {i:values.count(i) for i in values}

    # special case selection of all values:
    # when exactly the half of values are equal the other half needs to be the same = only two different values allowed
    # (e.g. 3 x 6 needs 3 x the same other values and not different values)
    if len(values) == MAX_DICE_COUNT and list(count_single_values.values())[0] == len(values) // 2 and len(count_single_values) != 2:
        return False
    
    # combinations are not possible when more then half values are equal but not all
    # (e.g. 3 x 6 for 4 values or 4 - 5 x 6 for 6 dice)
    for value_count in count_single_values.values():
        if value_count > len(values) // 2 and value_count < len(values):
            return False

    return True

def _get_valid_combination(values):
    combinations = set()

    # get all combinations which are equal for all values
    for i, value in enumerate(values):
        # save the current single value
        current_combinations = {value}
        # check all combinations
        for j, check_value in enumerate(values):
            # except the current value
            if j != i:
                current_combination = value + check_value
                if current_combination > MAX_DICE_COUNT:
                    current_combinations.add(current_combination)
        if i == 0:
            # save combinations for first number
            combinations = current_combinations
        else:
            # only save the combinations which are equal for all numbers
            combinations = combinations.intersection(current_combinations)

    return combinations

# combine every number with every other number
def _get_value_combinations(values):
    if len(values) == 0:
        return set()
        
    # combinations are not possible when the number of values is uneven
    if len(values) % 2 != 0:
        return _validate_uneven_count(values)
    
    if not _valid_special_combinations(values):
        return set()
        
    return _get_valid_combination(values)
