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

dice_img = {}
selected_dice_img = {}
current_dice = []
used_dice = []
buttons = []
scores = []

# load confirm button images only once on initialization for reuse
# 0 = enabled, 1 = disabled
confirm_btn_imgs = []

# TODO: Playername: Score: 1-12: 0-5

def highlight_score_numbers(numbers: [int] = []):
	scores[0].generate_text(numbers)

def enable_confirm_btn():
	if buttons[0].disabled:
		buttons[0] = button.Button(confirm_btn_imgs[0], 0.8, "confirm", SCREEN_SIZE, False)

def disable_confirm_btn():
	if not buttons[0].disabled:
		buttons[0] = button.Button(confirm_btn_imgs[1], 0.8, "confirm", SCREEN_SIZE, True)

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
	disable_confirm_btn()	

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

# combine every number with every other number
def get_value_combinations(values):
	if len(values) == 0:
		return set()
		
	# combinations are not possible when the number of values is uneven
	if len(values) % 2 != 0:
		# are all numbers equal? 
		# use set to group values and check length
		if len(set(values)) == 1:
			# return the number
			return {values[0]}
		else:
			return set()
	
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

def validate_selection():
	combinations = get_value_combinations(get_selected_current_dice_values())

	if len(combinations) == 0:
		highlight_score_numbers()
		return False

	if not is_first_move():
		# TODO for second move check if selection equals hightlighted score
		pass

	# TODO check if number already completed
	
	highlight_score_numbers(combinations)

	# TODO remove placeholder
	return True

# init images, buttons and dice instances for the first move
def init():
	# set game name
	pygame.display.set_caption('1 - 12')
	# global init (needed for fonts etc.)
	pygame.init()

	# init button images
	confirm_btn_imgs.append(pygame.image.load('img/button_confirm.png').convert_alpha())
	confirm_btn_imgs.append(pygame.image.load('img/button_confirm_disabled.png').convert_alpha())
	finish_btn_img = pygame.image.load('img/button_finish.png').convert_alpha()

	# init button instances
	buttons.append(button.Button(confirm_btn_imgs[0], 0.8, "confirm", SCREEN_SIZE))
	buttons.append(button.Button(finish_btn_img, 0.8, "finish", SCREEN_SIZE))

	# init scores # TODO multiplayer
	scores.append(score.Score(SCREEN_SIZE[0]))

	# init dice images
	for i in range(1, 7):
		dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
		selected_dice_img[i] = pygame.image.load('img/' + str(i) + '_selected.png').convert_alpha()

	move()

def main():
	init()

	#game loop
	run = True
	while run:
		# draw confirm button and listen to click
		if buttons[0].draw(SCREEN):
			set_selected_dice()
			move()

		# draw finish button and listen to click
		if buttons[1].draw(SCREEN):
			scores[0].update(get_used_dice_values())
			used_dice.clear()
			move()

		# draw all dice and listen to clicks in object
		for dice in current_dice:
			if dice.draw(SCREEN):
				if validate_selection():
					enable_confirm_btn()
				else:
					disable_confirm_btn()


		for dice in used_dice:
			dice.draw(SCREEN)

		# draw score #TODO for current player
		scores[0].draw(SCREEN)

		#event handler
		for event in pygame.event.get():
			pass
			#quit game (press X)
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

main()