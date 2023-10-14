import pygame

OFFSET = 15

#button class
class DrawOnlyDice():
	def __init__(self, img: pygame.image, value: int, index: int, scale: float):
		width = img.get_width() * scale
		self.pos = self.get_pos(index, width)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], width, width)
		self.img = pygame.transform.scale(img, (width, width))
		self.value = value

	def draw(self, surface):
		#draw button on screen
		surface.blit(self.img, (self.rect.x, self.rect.y))
	
	# calc pos for two rows in top left corner
	def get_pos(self, index: int, width: int) -> tuple:
		y = OFFSET
		if index >= 3:
			y += width + OFFSET
			index -= 3
		return (index * width + (index + 1) * OFFSET , y)