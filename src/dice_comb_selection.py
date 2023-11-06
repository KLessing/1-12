import pygame

OFFSET = 30

class DiceCombSelection():
	def __init__(self, screen_size):
		# TODO dynamic
		self.selection_btn_img = {}        
		self.selection_btn_img[4] = pygame.image.load('img/button_4.png').convert_alpha()
		self.selection_btn_img[5] = pygame.image.load('img/button_5.png').convert_alpha()
		self.selection_btn_img[6] = pygame.image.load('img/button_6.png').convert_alpha()
		self.selection_btn_img[8] = pygame.image.load('img/button_8.png').convert_alpha()
		self.selection_btn_img[10] = pygame.image.load('img/button_10.png').convert_alpha()
		self.selection_btn_img[12] = pygame.image.load('img/button_12.png').convert_alpha()

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

		rect = self.single_rect if number <= 6 else self.comb_rect

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