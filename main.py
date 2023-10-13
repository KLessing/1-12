import pygame
import clickable
import dice
import random

SCREEN_SIZE = (852, 480)

#create display window
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = pygame.image.load('img/table_top.png').convert_alpha()

pygame.display.set_caption('1 - 12')

dice_img = {}
selected_dice_img = {}
current_dice = {}

# init images and dice instances for the first move
def init():	
	# use background img, starting at rect top left
	SCREEN.blit(BACKGROUND, [0, 0])

	# init images
	for i in range(1, 7):
		dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
		selected_dice_img[i] = pygame.image.load('img/' + str(i) + '_selected.png').convert_alpha()

	# init first move
	for i in range(0, 6):
		rdm = random.randrange(1, 7) # rdm 1 - 6
		current_dice[i] = dice.Dice(dice_img[rdm], selected_dice_img[rdm], rdm, i, 6, SCREEN_SIZE)

def main():
	init()

	#game loop
	run = True
	while run:
		# placeholder: draw all dices instances for now
		for i in range(len(current_dice)):
			if current_dice[i].draw(SCREEN):
				print(current_dice[i].value, ":", current_dice[i].clicked)

		#event handler
		for event in pygame.event.get():
			pass
			#quit game (press X)
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

main()