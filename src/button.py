import pygame

OFFSET = 25

class Button():
	def __init__(self, img: pygame.image, scale: float, pos: str, screen_size: tuple, disabled_img: pygame.image = None):
		width = img.get_width() * scale
		height = img.get_height() * scale
		self.pos = self.get_pos(pos, screen_size, width, height)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], width, height)
		
		self.img = pygame.transform.scale(img, (width, height))
		if disabled_img != None:
			self.disabled_img = pygame.transform.scale(disabled_img, (width, height))

		self.clicked = False
		self.disabled = False

	def draw(self, surface):
		action = False

		if self.disabled:
			surface.blit(self.disabled_img, (self.rect.x, self.rect.y))
			# don't check click when disabled	
			return action
		
		surface.blit(self.img, (self.rect.x, self.rect.y))
		
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
	
	# calc pos for bottom mid
	def get_pos(self, pos: str, screen_size: tuple, width: int, height: int) -> tuple:
		return (screen_size[0] // 2 + (OFFSET if pos == "right" else - width - OFFSET),
		  		screen_size[1] - height - OFFSET)

	def enable(self):
		self.disabled = False

	def disable(self):
		self.disabled = True
		