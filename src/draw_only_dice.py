import pygame

OFFSET = 15

class DrawOnlyDice():
	def __init__(self, img: pygame.image, pos: tuple, value: int, width: int):
		self.rect = pygame.Rect(pos[0], pos[1], width, width)
		self.img = pygame.transform.scale(img, (width, width))
		self.value = value

	def draw(self, surface):
		#draw button on screen
		surface.blit(self.img, (self.rect.x, self.rect.y))