import pygame
import clickable
import dice
import random

SCREEN_SIZE = (852, 480)
OFFSET = 30
IMG_WIDTH = 100

#create display window
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = pygame.image.load('img/table_top.png').convert_alpha()

pygame.display.set_caption('1 - 12')

dice_img = {}
selected_dice_img = {}
current_dice = {}

# calc dice pos dynamically in screen mid according to dice index and count of all dice
def get_dice_pos(index: int, count: int = 6) -> tuple:
	# separate all dice into two rows
	# round down to whole number with //
	separator = count // 2 
	height_mid = SCREEN_SIZE[1] // 2
	
	if count == 1:
		# single dice
		y = height_mid - (IMG_WIDTH // 2)
		col_index = 0 # the index in the row
		col_count = 1 # how many columns (dice) are in the row
	elif index < separator:
		# top row
		y = height_mid - IMG_WIDTH - (OFFSET // 2)
		col_index = index
		col_count = separator
	else:
		# bottom row
		y = height_mid + (OFFSET // 2)
		col_index = index - separator
		col_count = count - separator

	dice_row_width = col_count * IMG_WIDTH + (col_count - 1) * OFFSET
	dice_row_pos = (SCREEN_SIZE[0] // 2) - (dice_row_width // 2)
	x = col_index * (IMG_WIDTH + OFFSET) + dice_row_pos
		
	return (x, y)

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
		pos = get_dice_pos(i)
		current_dice[i] = dice.Dice(pos[0], pos[1], dice_img[rdm], selected_dice_img[rdm], rdm)

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