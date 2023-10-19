import pygame

OFFSET = 15
LINE_OFFSET = 30
WIDTH = 100
HEIGTH = 500

STANDARD_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (0, 0, 0)

class SCORE():
	def __init__(self, values: [str], screen_width: int, highlights: [int] = []):
		self.x = screen_width - WIDTH + OFFSET
		self.values = values

		# use default font (init needed)
		font = pygame.font.Font(None, 30) 

		self.text = []
		for key, value in values.items():
			txt = str(key) + " : " + str(value)
			if key < 10:
				# indent one-digit numbers
				txt = ' ' + txt
			if key in highlights:
				self.text.append(font.render(txt , True, HIGHLIGHT_COLOR))
			else:
				self.text.append(font.render(txt , True, STANDARD_COLOR))

	def draw(self, surface):
		for line, text in enumerate(self.text):
			pos = self.get_pos(line)
			rect = pygame.Rect(pos[0], pos[1], WIDTH, HEIGTH)
			surface.blit(text, rect)
	
	def get_pos(self, line) -> tuple:
		return (self.x , line * LINE_OFFSET + OFFSET)