import pygame

import utils.globals as globals

OFFSET = 30
MAX = 15

class Dice():
	def __init__(self, imgs: [pygame.image], s_img: pygame.image, value: int, pos: tuple):
		self.rect = pygame.Rect(pos[0], pos[1], globals.IMG_SIZE, globals.IMG_SIZE)
		self.imgs = imgs
		self.s_img = s_img
		self.value = value
		self.clicked = False
		self.animationStep = 0

	def listen_for_click(self) -> bool:
		# Get mouse position
		pos = pygame.mouse.get_pos()

		# Check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = not self.clicked
				# delay to prevent multi action for one click
				# (e.g. constant selection and deselection while button is pressed)
				pygame.time.delay(globals.CLICK_DELAY_MS)
				return True
		
		return False

	def draw(self, surface: pygame.display):
		if self.clicked:
			surface.blit(self.s_img, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.imgs[self.animationStep], (self.rect.x, self.rect.y))
		
		if self.animationStep < MAX:
			self.animationStep += 1
