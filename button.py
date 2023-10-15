import pygame

OFFSET = 25

class Button():
	def __init__(self, img: pygame.image, scale: float, value: str, screen_size: tuple, disabled: bool = False):
		width = img.get_width() * scale
		height = img.get_height() * scale
		self.pos = self.get_pos(value, screen_size, width, height)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], width, height)
		self.img = pygame.transform.scale(img, (width, height))
		self.clicked = False
		self.disabled = disabled

	def draw(self, surface):
		action = False

		# draw button on screen
		surface.blit(self.img, (self.rect.x, self.rect.y))

		# don't check click when disabled
		if self.disabled:
			return action
		
		# get mouse position
		pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action
	
	# calc pos for bottom corner: confirm right corner, finish left corner
	def get_pos(self, value: str, screen_size: tuple, width: int, height: int) -> tuple:
		y = screen_size[1] - height - OFFSET
		if value == "confirm":
			return (screen_size[0] - width - OFFSET, y)
		elif value == "finish":
			return (OFFSET, y)