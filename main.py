import pygame
import button
import dice
import draw_only_dice
import random

SCREEN_SIZE = (852, 480)

#create display window
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = pygame.image.load('img/table_top.png').convert_alpha()

pygame.display.set_caption('1 - 12')

dice_img = {}
selected_dice_img = {}
current_dice = []
used_dice = []
buttons = []

def move():
	# reset screen to draw new dice instances without overlapping
	SCREEN.blit(BACKGROUND, [0, 0])
	count = 6 - len(used_dice)
	current_dice.clear()
	for i in range(0, count):
		rdm = random.randrange(1, 7) # rdm 1 - 6
		current_dice.append(dice.Dice(dice_img[rdm], selected_dice_img[rdm], rdm, i, count, SCREEN_SIZE))

def set_selected_dice():
	selected_dice = []

	for dice in used_dice:
		selected_dice.append(dice.value)

	for dice in current_dice:
		if dice.clicked:
			selected_dice.append(dice.value)

	used_dice.clear()
	selected_dice.sort(reverse=True)

	for index, value in enumerate(selected_dice):
		used_dice.append(draw_only_dice.DrawOnlyDice(dice_img[value], value, index, len(selected_dice), 0.5))

# init images, buttons and dice instances for the first move
def init():
	# use background img, starting at rect top left
	SCREEN.blit(BACKGROUND, [0, 0])

	# init button images
	confirm_btn_img = pygame.image.load('img/button_confirm.png').convert_alpha()
	finish_btn_img = pygame.image.load('img/button_finish.png').convert_alpha()

	# init button instances
	buttons.append(button.Button(confirm_btn_img, 0.75, "confirm", SCREEN_SIZE))
	buttons.append(button.Button(finish_btn_img, 0.75, "finish", SCREEN_SIZE))

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
			used_dice.clear()
			move()

		# draw all dice and listen to clicks
		for dice in current_dice:
			dice.draw(SCREEN)

		for dice in used_dice:
			dice.draw(SCREEN)

		#event handler
		for event in pygame.event.get():
			pass
			#quit game (press X)
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

main()