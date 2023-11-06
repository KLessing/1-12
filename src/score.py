import pygame

OFFSET = 15
LINE_OFFSET = 37
LINE_CENTER = 10
WIDTH = 370
HEIGTH = 540

DEFAULT_COLOR = (255, 255, 255)
SELECTED_COLOR = (0, 0, 0)

class Score():
	def __init__(self, player_name: str, player_index: int, screen_width: int):
		self.selections = set()
		self.continue_move = False
		self.win = False
		self.is_active = False

		# score is drawn in the top right
		# 5 columns, first column contains the number, start at second column for each player index
		# TODO player index param
		# TODO Cut Player name to 5 chars
		# TODO Max Const
		column_size = WIDTH // 5
		max_player_index = 4
		self.x_pos = screen_width - (column_size * (max_player_index - player_index) - OFFSET)

		# init values
		self.values = {}
		for i in range(1, 13):
			self.values[i] = 0

		self.player_name = player_name
		player_font = pygame.font.Font(None, 42)
		self.player_text = player_font.render(player_name , True, DEFAULT_COLOR)
		self.player_rect = self.player_text.get_rect(center=(screen_width/2, LINE_OFFSET + OFFSET))

		# use default font for score (init needed)
		self.score_font = pygame.font.Font(None, 30)
		self.player_font = pygame.font.Font(None, 24)
		self.text = []
		self.generate_text()

	def draw(self, surface: pygame.display):
		# draw player name to top middle when active
		if self.is_active:
			surface.blit(self.player_text, self.player_rect)

		# draw score
		for line, text in enumerate(self.text):
			pos = self.get_pos(line)
			rect = pygame.Rect(pos[0], pos[1], WIDTH, HEIGTH)
			surface.blit(text, rect)
	
	def get_pos(self, line: str) -> tuple:
		return (self.x_pos , line * LINE_OFFSET + LINE_CENTER)
	
	# selection = highlight these numbers
	# (empty param = only standard colored numbers)
	def generate_text(self):
		win = True
		self.text = []
		self.text.append(self.player_font.render(self.player_name, True, DEFAULT_COLOR))
		for key, value in self.values.items():
			txt = ""
			# add stroke for every collected value
			for i in range(value):
				txt += "|"
			if value != 5:
				win = False
				if key in self.selections:
					self.text.append(self.score_font.render(txt , True, SELECTED_COLOR))
				else:
					self.text.append(self.score_font.render(txt , True, DEFAULT_COLOR))
			else:
				# strike through 4 strokes
				self.score_font.set_strikethrough(True)
				self.text.append(self.score_font.render(txt[:-1] , True, DEFAULT_COLOR))
				self.score_font.set_strikethrough(False)
				
		self.win = win

	# update the score after the move is finished
	# (selection will be removed)
	def update(self, used_dice_count: int):
		# nothing selected = no update
		if used_dice_count == 0:
			self.continue_move = False
			return

		# score count which is added to the score value
		score_count = used_dice_count

		# uneven count of used dice or combination already full?
		if used_dice_count % 2 == 1 or self.values[max(self.selections)] == 5:
			# get single value (e.g. 5 5 5 instead of 10)
			real_selection = min(self.selections)
		else:
			# otherwise use the number comb (e.g. 10 instead of 5)
			real_selection = max(self.selections)

			if real_selection >= 7:		
				# two dice are used for one number comb
				score_count = used_dice_count // 2
		
		# add to score until max is reached
		if self.values[real_selection] + score_count <= 5:
			self.values[real_selection] += score_count
		else:
			# when the addition would be higher than five: cut to 5
			self.values[real_selection] = 5

		# continue move when all dice are used or collection is full
		self.continue_move = used_dice_count == 6 or self.values[real_selection] == 5
		
		# reset selection for next player move or when collection is full
		if not self.continue_move or self.values[real_selection] == 5:
			self.set_selection()

		self.generate_text()		

	def set_selection(self, selection: set = set()):
		self.selections = selection
		# reset text for hightlighting
		self.generate_text()

	def get_completed_values(self):
		completed = set()
		for i in range(1, 13):
			if self.values[i] == 5:
				completed.add(i)
		return completed
		
	def set_active(self, active: bool):
		self.is_active = active