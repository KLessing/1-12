import pygame

OFFSET = 15
LINE_OFFSET = 30
WIDTH = 100
HEIGTH = 500

DEFAULT_COLOR = (255, 255, 255)
SELECTED_COLOR = (0, 0, 0)
COMPLETED_COLOR = (100, 100, 100)

class Score():
	def __init__(self, player_name: str, screen_width: int):
		self.selections = set()
		self.x_pos = screen_width - WIDTH + OFFSET

		# init values
		self.values = {}
		for i in range(1, 13):
			self.values[i] = 0

		# use default font (init needed)
		self.font = pygame.font.Font(None, 30)
		self.text = []
		self.generate_text()

		player_font = pygame.font.Font(None, 42)
		self.player_text = player_font.render(player_name , True, DEFAULT_COLOR)
		self.player_rect = self.player_text.get_rect(center=(screen_width/2, LINE_OFFSET + OFFSET))

	def draw(self, surface: pygame.display):
		# draw player name
		surface.blit(self.player_text, self.player_rect)

		# draw score
		for line, text in enumerate(self.text):
			pos = self.get_pos(line)
			rect = pygame.Rect(pos[0], pos[1], WIDTH, HEIGTH)
			surface.blit(text, rect)
	
	def get_pos(self, line: str) -> tuple:
		return (self.x_pos , line * LINE_OFFSET + OFFSET)
	
	# selection = highlight these numbers
	# (empty param = only standard colored numbers)
	def generate_text(self):
		self.text = []
		for key, value in self.values.items():
			txt = str(key) + " : " + str(value)
			if key < 10:
				# indent one-digit numbers
				txt = ' ' + txt
			if value == 5:
				self.text.append(self.font.render(txt , True, COMPLETED_COLOR))
			elif key in self.selections:
				self.text.append(self.font.render(txt , True, SELECTED_COLOR))
			else:
				self.text.append(self.font.render(txt , True, DEFAULT_COLOR))

	# update the score after the move is finished
	# (selection will be removed)
	def update(self, used_dice_count: int):
		# nothing selected = no update
		if used_dice_count == 0:
			return

		# uneven count of used dice or combination already full?
		if used_dice_count % 2 == 1 or self.values[max(self.selections)] == 5:
			# get single value (e.g. 5 5 5 instead of 10)
			real_selection = min(self.selections)
		else:
			# otherwise use the number comb (e.g. 10 instead of 5)
			real_selection = max(self.selections)

			if real_selection >= 7:		
				# two dice are used for one number comb
				used_dice_count = used_dice_count // 2
		
		# add to score until max is reached
		if self.values[real_selection] + used_dice_count <= 5:
			self.values[real_selection] += used_dice_count
		else:
			self.values[real_selection] = 5

		# reset selection
		self.selections = set()
		self.generate_text()
		

	def set_selection(self, selection: set = set()):
		self.selections = selection
		# reset text for hightlighting
		self.generate_text()
			