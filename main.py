import pygame
import button
import dice
import draw_only_dice
import score
import random

SCREEN_SIZE = (852, 480)

#create display window
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = pygame.image.load('img/table_top.png').convert_alpha()

PLAYER_NAMES = ["Player 1", "Player 2"]

dice_img = {}
selected_dice_img = {}
current_dice = []
used_dice = []
scores = []

confirm_btn = {}
finish_btn = {}

current_player_index = 0

def use_test_values():
	test_values = [2, 2, 6, 6, 6, 6]
	#test_values = [6, 6, 6, 1, 4, 3]
	for i, val in enumerate(test_values):
		current_dice.append(dice.Dice(dice_img[val], selected_dice_img[val], val, i, len(test_values), SCREEN_SIZE))

def set_next_player():
	# use global var for overwriting
	global current_player_index

	if current_player_index == len(PLAYER_NAMES) - 1:
		current_player_index = 0
	else:
		current_player_index += 1

def move():
	# reset screen to draw the background image for new dice instances without overlapping
	SCREEN.blit(BACKGROUND, [0, 0])
	count = 6 - len(used_dice)
	current_dice.clear()
	for i in range(0, count):
		# roll dice (1-6)
		rdm = random.randrange(1, 7) 
		current_dice.append(dice.Dice(dice_img[rdm], selected_dice_img[rdm], rdm, i, count, SCREEN_SIZE))
	# disable confirm button before any selection
	confirm_btn.disable()

def end_move():
	# update score for current player
	scores[current_player_index].update(len(used_dice))
	
	# check if the user can continue with the next move
	if not scores[current_player_index].check_continue_move():
		# otherwise it's the next players turn
		set_next_player()
	
	# start new first move
	used_dice.clear()
	move()

def is_first_move():
	return len(used_dice) == 0

def get_selected_current_dice_values():
	return [dice.value for dice in current_dice if dice.clicked]

def get_used_dice_values():
	return [dice.value for dice in used_dice]

def get_all_selected_dice_values():
	res = get_selected_current_dice_values() + get_used_dice_values()
	return sorted(res, reverse=True)

def set_selected_dice():
	selected_dice_values = get_all_selected_dice_values()
	used_dice.clear()

	for index, value in enumerate(selected_dice_values):
		used_dice.append(draw_only_dice.DrawOnlyDice(dice_img[value], value, index, 0.5))

def validate_uneven_count(values):
	# are all numbers equal? 
	# use set to group values and check length
	if len(set(values)) == 1:
		# return the number
		return {values[0]}
	else:
		return set()

def valid_special_combinations(values):
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

def get_valid_combination(values):
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
def get_value_combinations(values):
	if len(values) == 0:
		return set()
		
	# combinations are not possible when the number of values is uneven
	if len(values) % 2 != 0:
		return validate_uneven_count(values)
	
	if not valid_special_combinations(values):
		return set()
		
	return get_valid_combination(values)

def validate_selection():
	combinations = get_value_combinations(get_selected_current_dice_values())
	combinations = scores[current_player_index].remove_collected_values(combinations)

	if not is_first_move():
		# check combinations with already selected values
		combinations = combinations.intersection(scores[current_player_index].selections)
		# only update selection when changed 
		# (e.g. first move 5 5, second move 5, now only single 5 is selected instead of 10)
		if len(combinations) >= 1:
			scores[current_player_index].set_selection(combinations)
	else:
		# selection will stay after first move
		scores[current_player_index].set_selection(combinations)

	if len(combinations) == 0:
		return False
	else:
		return True

# init images, buttons and dice instances for the first move
def init():
	# set game name
	pygame.display.set_caption('1 - 12')
	# global init (needed for fonts etc.)
	pygame.init()

	# init button images
	confirm_btn_enabled_img = pygame.image.load('img/button_confirm.png').convert_alpha()
	confirm_btn_disabled_img = pygame.image.load('img/button_confirm_disabled.png').convert_alpha()
	finish_btn_img = pygame.image.load('img/button_finish.png').convert_alpha()

	# init global button instances
	global confirm_btn, finish_btn
	confirm_btn = button.Button(confirm_btn_enabled_img, 0.8, "confirm", SCREEN_SIZE, confirm_btn_disabled_img)
	finish_btn = button.Button(finish_btn_img, 0.8, "finish", SCREEN_SIZE)

	# init scores for all players
	for player_name in PLAYER_NAMES:
		scores.append(score.Score(player_name, SCREEN_SIZE[0]))

	# init dice images
	for i in range(1, 7):
		dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
		selected_dice_img[i] = pygame.image.load('img/' + str(i) + '_selected.png').convert_alpha()

	# start first move
	move()

def main():
	init()

	#game loop
	run = True
	while run:
		# draw confirm button and listen to click
		if confirm_btn.draw(SCREEN):
			set_selected_dice()
			move()

		# draw finish button and listen to click
		if finish_btn.draw(SCREEN):
			end_move()

		# draw all dice and listen to clicks in object
		for dice in current_dice:
			if dice.draw(SCREEN):
				if validate_selection():
					confirm_btn.enable()
				else:
					confirm_btn.disable()


		for dice in used_dice:
			dice.draw(SCREEN)

		# draw score for current player
		scores[current_player_index].draw(SCREEN)

		#event handler
		for event in pygame.event.get():
			pass
			#quit game (press X)
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

main()