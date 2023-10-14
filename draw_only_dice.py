import pygame

OFFSET = 15

#button class
class DrawOnlyDice():
	def __init__(self, img: pygame.image, value: int, index: int, count: int, scale: float):
		width = img.get_width() * scale
		height = img.get_height() * scale
		self.pos = self.get_pos(index, width, height)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], width, height)
		self.img = pygame.transform.scale(img, (width, height))
		self.value = value

	def draw(self, surface):
		#draw button on screen
		surface.blit(self.img, (self.rect.x, self.rect.y))
	
	# calc pos for bottom corner: confirm right corner, finish left corner
	def get_pos(self, index: int, count: int, width: int) -> tuple:		
		return (index * width + (index + 1) * OFFSET , OFFSET)