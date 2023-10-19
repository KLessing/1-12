import pygame

OFFSET = 15
LINE_OFFSET = 30
WIDTH = 100
HEIGTH = 500

DEFAULT_COLOR = (255, 255, 255)
SELECTED_COLOR = (0, 0, 0)
COMPLETED_COLOR = (100, 100, 100)

class Score():
	def __init__(self, screen_width: int):
		self.x = screen_width - WIDTH + OFFSET
		self.values = {}
		for i in range(1, 13):
			self.values[i] = 0

		# use default font (init needed)
		self.font = pygame.font.Font(None, 30)
		self.text = []
		self.generate_text()

	def draw(self, surface: pygame.display):
		for line, text in enumerate(self.text):
			pos = self.get_pos(line)
			rect = pygame.Rect(pos[0], pos[1], WIDTH, HEIGTH)
			surface.blit(text, rect)
	
	def get_pos(self, line: str) -> tuple:
		return (self.x , line * LINE_OFFSET + OFFSET)
	
	# selection = highlight these numbers
	# (empty param = only standard colored numbers)
	def generate_text(self, selection: [int] = []):
		self.text = []
		for key, value in self.values.items():
			txt = str(key) + " : " + str(value)
			if key < 10:
				# indent one-digit numbers
				txt = ' ' + txt
			if value == 5:
				self.text.append(self.font.render(txt , True, COMPLETED_COLOR))
			elif key in selection:
				self.text.append(self.font.render(txt , True, SELECTED_COLOR))
			else:
				self.text.append(self.font.render(txt , True, DEFAULT_COLOR))

	# update the score after the move is finished
	# (selection will be removed)
	def update(self, values: [int]):	
		for value in values:
			if self.values[value] < 5:
				self.values[value] += 1
		self.generate_text()
			