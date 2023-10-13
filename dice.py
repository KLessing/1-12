import pygame

# Dice class
class Dice():
	def __init__(self, x, y, img, s_img, value):
		self.rect = pygame.Rect(x, y, img.get_width(), img.get_height())
		self.img = img
		self.s_img = s_img
		self.clicked = False
		self.value = value

	def draw(self, surface):
		action = False
		# Get mouse position
		pos = pygame.mouse.get_pos()

		# Check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = not self.clicked
				# prevent click trigger for two seconds
				pygame.time.delay(200)
				action = True

		# Draw Clickable img on screen
		if self.clicked:
			surface.blit(self.s_img, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.img, (self.rect.x, self.rect.y))

		return action