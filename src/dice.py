import pygame

from utils.globals import CLICK_DELAY_MS

OFFSET = 30

class Dice():
	def __init__(self, img: pygame.image, s_img: pygame.image, value: int, index: int, count: int, screen_size: tuple):
		width = img.get_width()
		self.pos = self.get_pos(index, count, screen_size, width)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], width, width)
		self.img = img
		self.s_img = s_img
		self.value = value
		self.clicked = False

	def listen_for_click(self) -> bool:
		# Get mouse position
		pos = pygame.mouse.get_pos()

		# Check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = not self.clicked
				# delay to prevent multi action for one click
				# (e.g. constant selection and deselection while button is pressed)
				pygame.time.delay(CLICK_DELAY_MS)
				return True
		
		return False

	def draw(self, surface: pygame.display):
		if self.clicked:
			surface.blit(self.s_img, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.img, (self.rect.x, self.rect.y))

	# calc dice pos dynamically in screen mid according to dice index and count of all dice
	def get_pos(self, index: int, count: int, screen_size: tuple, width: int) -> tuple:
		# separate all dice into two rows
		# round down to whole number with //
		separator = count // 2 
		height_mid = screen_size[1] // 2
		
		if count == 1:
			# single dice
			y = height_mid - (width // 2)
			col_index = 0 # the index in the row
			col_count = 1 # how many columns (dice) are in the row
		elif index < separator:
			# top row
			y = height_mid - width - (OFFSET // 2)
			col_index = index
			col_count = separator
		else:
			# bottom row
			y = height_mid + (OFFSET // 2)
			col_index = index - separator
			col_count = count - separator

		dice_row_width = col_count * width + (col_count - 1) * OFFSET
		dice_row_pos = (screen_size[0] // 2) - (dice_row_width // 2)
		x = col_index * (width + OFFSET) + dice_row_pos
			
		return (x, y)	