import pygame

from utils.globals import CLICK_DELAY_MS

class DrawOnlyDice():
	def __init__(self, img: pygame.image, pos: tuple, value: int, width: int):
		self.rect = pygame.Rect(pos[0], pos[1], width, width)
		self.img = pygame.transform.scale(img, (width, width))
		self.value = value

	def draw(self, surface):
		#draw button on screen
		surface.blit(self.img, (self.rect.x, self.rect.y))

	def listen_for_click(self) -> bool:
		# Get mouse position
		pos = pygame.mouse.get_pos()
		clicked = pygame.mouse.get_pressed()[0]

		# check left click and mouse pos collide
		if clicked and self.rect.collidepoint(pos):
			return True
		
		return False