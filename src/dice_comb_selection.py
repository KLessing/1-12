import pygame
from utils.globals import MAX_DICE_COUNT

OFFSET = 30
# all dice numbers with corresponding double combination
RELEVANT_NUMBERS = [4, 5, 6, 8, 10, 12]

class DiceCombSelection():
	def __init__(self, screen_size):
		self.selection_btn_img = {}
		for i in RELEVANT_NUMBERS:
			self.selection_btn_img[i] = pygame.image.load(f"img/button_{i}.png").convert_alpha()

		# width is equal for all images
		width = self.selection_btn_img[4].get_width()
		top_pos = self.get_pos(True, screen_size, width)
		bottom_pos = self.get_pos(False, screen_size, width)
		self.single_rect = pygame.Rect(top_pos[0], top_pos[1], width, width)
		self.comb_rect = pygame.Rect(bottom_pos[0], bottom_pos[1], width, width)

	def draw(self, number: int, surface: pygame.display):
		action = False
		# Get mouse position
		pos = pygame.mouse.get_pos()

		rect = self.single_rect if number <= MAX_DICE_COUNT else self.comb_rect

		# Check mouseover and clicked conditions
		if rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
				# prevent click trigger for two seconds
				pygame.time.delay(200)

		# Draw Clickable img on screen
		surface.blit(self.selection_btn_img[number], (rect.x, rect.y))

		return action

	# calc dice pos dynamically in screen mid according to dice index and count of all dice
	# top: True = top y pos, False = bottom y pos
	def get_pos(self, top: bool, screen_size: tuple, width: int) -> tuple:
		x = screen_size[0] // 2 - width // 2
		height_mid = screen_size[1] // 2
		
		# Single number to top, comp bottom
		if top:
			# top row
			y = height_mid - width - (OFFSET // 2)
		else:
			# bottom row
			y = height_mid + (OFFSET // 2)
			
		return (x, y)	