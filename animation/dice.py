import pygame

import utils.globals as globals

OFFSET = 30
MAX = 15

class Dice():
	def __init__(self, imgs: [pygame.image], s_img: pygame.image, value: int, pos: tuple, delay: int):
		self.rect = pygame.Rect(pos[0], pos[1], globals.IMG_SIZE, globals.IMG_SIZE)
		self.imgs = imgs
		self.s_img = s_img
		self.value = value
		self.clicked = False
		self.animationStep = 0
		self.delay = delay
		self.delayer = 0

	def listen_for_click(self) -> bool:
		if self.animationStep < MAX:
			return False

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
		if self.animationStep < MAX:
			if self.delayer < self.delay:
				self.delayer += 1
			else:
				self.animationStep += 1
				self.delayer = 0

		if self.clicked:
			surface.blit(self.s_img, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.imgs[self.animationStep], (self.rect.x, self.rect.y))

