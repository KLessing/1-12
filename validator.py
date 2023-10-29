import score

class Validator():
    def validate_uneven_count(self, values):
        # are all numbers equal? 
        # use set to group values and check length
        if len(set(values)) == 1:
            # return the number
            return {values[0]}
        else:
            return set()

    def valid_special_combinations(self, values):
        # check individual values for special cases
        count_single_values = {i:values.count(i) for i in values}

        # when exactly the half of values are equal the other half needs to be the same = only two different values allowed
        # (e.g. 3 x 6 needs 3 x the same other values and not different values)
        if list(count_single_values.values())[0] == len(values) // 2 and len(count_single_values) != 2:
            return False
        
        # combinations are not possible when more then half values are equal but not all
        # (e.g. 3 x 6 for 4 values or 4 - 5 x 6 for 6 dice)
        for value_count in count_single_values.values():
            if value_count > len(values) // 2 and value_count < len(values):
                return False

        return True

    def get_valid_combination(self, values):
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
                    if current_combination >= 7:
                        current_combinations.add(current_combination)
            if i == 0:
                # save combinations for first number
                combinations = current_combinations
            else:
                # only save the combinations which are equal for all numbers
                combinations = combinations.intersection(current_combinations)

        return combinations

    # combine every number with every other number
    def get_value_combinations(self, values):
        if len(values) == 0:
            return set()
            
        # combinations are not possible when the number of values is uneven
        if len(values) % 2 != 0:
            return self.validate_uneven_count(values)
        
        if not self.valid_special_combinations(values):
            return set()
            
        return self.get_valid_combination(values)

    def validate_selection(self, selection: [int], score: score.Score, first_move: bool):
        combinations = self.get_value_combinations(selection)
        combinations = score.remove_collected_values(combinations)

        if not first_move:
            # check combinations with already selected values
            combinations = combinations.intersection(score.selections)
            # only update selection when changed 
            # (e.g. first move 5 5, second move 5, now only single 5 is selected instead of 10)
            if len(combinations) >= 1:
                score.set_selection(combinations)
        else:
            # selection will stay after first move
            score.set_selection(combinations)

        if len(combinations) == 0:
            return False
        else:
            return True