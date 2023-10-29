import pygame
import button
import dice
import draw_only_dice
import score
import validator
import random

SCREEN_SIZE = (852, 480)

#create display window
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = pygame.image.load('img/table_top.png').convert_alpha()

PLAYER_NAMES = ["Player 1", "Player 2"]

TEST_MODUS = False

dice_img = {}
selected_dice_img = {}
current_dice = []
used_dice = []
scores = []
validation = validator.Validator()

confirm_btn = {}
finish_btn = {}

current_player_index = 0

def use_test_values(count: int):
	test_values = [6, 1, 4, 3, 5, 2]
	for i in range(0, count):
		val = test_values[i]
		current_dice.append(dice.Dice(dice_img[val], selected_dice_img[val], val, i, count, SCREEN_SIZE))

def set_next_player():
	# use global var for overwriting
	global current_player_index

	if current_player_index == len(PLAYER_NAMES) - 1:
		current_player_index = 0
	else:
		current_player_index += 1

def roll_dice(count: int):
	for i in range(0, count):
		# roll dice (1-6)
		rdm = random.randrange(1, 7) 
		current_dice.append(dice.Dice(dice_img[rdm], selected_dice_img[rdm], rdm, i, count, SCREEN_SIZE))

def move():
	# reset screen to draw the background image for new dice instances without overlapping
	SCREEN.blit(BACKGROUND, [0, 0])
	count = 6 - len(used_dice)
	current_dice.clear()
	roll_dice(count) if not TEST_MODUS else use_test_values(count)
	# disable confirm button before any selection
	confirm_btn.disable()

def end_move():
	# update score for current player
	scores[current_player_index].update(len(used_dice))
	
	# check if the user can continue with the next move
	if not scores[current_player_index].continue_move:
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
	
def draw_win_screen():
	winner_font = pygame.font.Font(None, 72)
	winner_text = winner_font.render("YOU WIN!" , True, (255, 255, 255))
	winner_rect = winner_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
	SCREEN.blit(winner_text, winner_rect)

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

def validate_selection():
	if validation.validate_selection(get_selected_current_dice_values(), scores[current_player_index], is_first_move()):
		confirm_btn.enable()
	else:
		confirm_btn.disable()

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

		if scores[current_player_index].win:
			draw_win_screen()
		else:
			# draw all dice and listen to clicks in object
			for dice in current_dice:
				if dice.draw(SCREEN):
					validate_selection()

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