import pygame

from utils.globals import CLICK_DELAY_MS

OFFSET = 30

class Dice():
	def __init__(self, img: pygame.image, s_img: pygame.image, value: int, pos: tuple):
		width = img.get_width()
		self.rect = pygame.Rect(pos[0], pos[1], width, width)
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
