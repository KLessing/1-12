import pygame
import clickable

#create display window
SCREEN_WIDTH = 852
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('1 - 12')

offset_y = 175
offset_x = 25
img_width = 100

dice_img = {}
dice_instance = {}

def get_dice_pos(index: int, count: int = 6):
	# x = img width = 100 pixel; 25 pixel between images, starting at 25 pixel to left border
	# y = offset for now
	return ((img_width + offset_x) * (i - 1) + offset_x, offset_y)

# load images and dice instances
def load():	
	background = pygame.image.load('img/table_top.png').convert_alpha()

	for i in range(1, 7):
		dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
		pos = get_dice_pos(i)
		dice_instance[i] = clickable.Clickable(pos[0], pos[1], dice_img[i], 1)

#game loop
run = True
while run:

	# color backround
	screen.fill([255, 255, 255]) 

	# use background img, starting at rect top left
	#screen.blit(background, [0, 0])

	# placeholder: draw all dices instances for now
	for i in range(1, 7):
		if dice_instance[i].draw(screen):
			print(i)

	#event handler
	for event in pygame.event.get():
		pass
		#quit game (press X)
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()