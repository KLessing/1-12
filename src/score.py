import pygame

from utils.globals import MAX_DICE_COUNT

MAX_PLAYER_COUNT = 4

Y_OFFSET = 100

SCORE_OFFSET = 50
CELL_HEIGHT = 36
CELL_X_OFFSET = 25
CELL_Y_OFFSET = 10

DEFAULT_COLOR = (255, 255, 255)
SELECTED_COLOR = (255, 0, 0)
FINISHED_COLOR = (0, 255, 0)

class Score():
	def __init__(self, player_index: int, screen_width: int):
		self.current_selection = None
		self.is_active = False
		self.collected_count = 0
		# rest values sum for each lost game
		self.global_score = 0

		# convert alpha to keep transparency (while optimizing blitting)
		self.score_img = pygame.image.load('img/score-trans_375x510.png').convert_alpha()
		# center right horizontally and align to playername vertically
		self.score_pos = (screen_width - self.score_img.get_width() - SCORE_OFFSET, Y_OFFSET + CELL_Y_OFFSET)

		# 5 columns, first column contains the number, start at second column for each player index
		cell_width = self.score_img.get_width() // 5
		self.player_score_x_pos = self.score_img.get_width() - (cell_width * (MAX_PLAYER_COUNT - player_index) - CELL_X_OFFSET)

		self.player_index = player_index
		player_name = "PLAYER " + str(self.player_index + 1)
		player_font = pygame.font.Font(None, 42)
		self.player_text = player_font.render(player_name , True, DEFAULT_COLOR)
		self.player_rect = self.player_text.get_rect(center=(screen_width/2, Y_OFFSET + CELL_HEIGHT))

		# use default font for score (init needed)
		self.score_font = pygame.font.Font(None, 30)
		self.player_font = pygame.font.Font(None, 24)
		self.text = []

		# init values and generate text
		self.reset_values()
		self.generate_text()

	def draw(self, surface: pygame.display):
		# draw player name to top middle when active
		if self.is_active:
			surface.blit(self.player_text, self.player_rect)

		# draw score
		for line, text in enumerate(self.text):
			pos = self.get_pos(line)
			self.score_img.blit(text, pos)

		surface.blit(self.score_img, self.score_pos)
	
	def get_pos(self, line: str) -> tuple:
		return (self.player_score_x_pos , line * CELL_HEIGHT + CELL_Y_OFFSET)
	
	# selection = highlight these numbers
	# (empty param = only standard colored numbers)
	def generate_text(self) -> bool:
		win = True
		player_index_color = SELECTED_COLOR if self.is_active else DEFAULT_COLOR
		self.text = [self.player_font.render("P" + str(self.player_index + 1), True, player_index_color)]

		for key, value in self.values.items():
			txt = ""
			# add stroke for every collected value
			for i in range(value):
				txt += "|"
			if value != 5:
				win = False
				score_color = SELECTED_COLOR if key == self.current_selection else DEFAULT_COLOR
				self.text.append(self.score_font.render(txt , True, score_color))
			else:
				# strike through 4 strokes
				self.score_font.set_strikethrough(True)
				self.text.append(self.score_font.render(txt[:-1] , True, FINISHED_COLOR))
				self.score_font.set_strikethrough(False)

		if self.global_score > 0:
			self.text.append(self.score_font.render("- " + str(self.global_score) , True, DEFAULT_COLOR))

		return win

	# update the score after the move is finished
	# (selection will be removed)
	def update(self, used_dice_count: int) -> bool:
		current_used_dice_count = used_dice_count - self.collected_count
		self.collected_count += current_used_dice_count

		# score count which is added to the score value
		score_count = current_used_dice_count

		if self.current_selection > MAX_DICE_COUNT:		
			# two dice are used for one number comb
			score_count = current_used_dice_count // 2
		
		# add to score until max is reached
		if self.values[self.current_selection] + score_count <= 5:
			self.values[self.current_selection] += score_count
		else:
			# when the addition would be higher than five: cut to 5
			self.values[self.current_selection] = 5			

		return self.generate_text()

	def set_selection(self, selection: int = None):
		self.current_selection = selection
		self.generate_text()

	def get_completed_values(self):
		completed = set()
		for i in range(1, 13):
			if self.values[i] == 5:
				completed.add(i)
		return completed
	
	def is_selection_complete(self):
		return self.values[self.current_selection] == 5
		
	def set_active(self, active: bool):
		self.is_active = active
		self.generate_text()

	def reset_collected_count(self):
		self.collected_count = 0

	def calc_global_score(self):
		for key, value in self.values.items():
			self.global_score += key * (5 - value)
		self.generate_text()

	def reset_values(self):
		self.values = {}
		for i in range(1, 13):
			self.values[i] = 0
