import pygame

from .dice import Dice


OFFSET = 15
LINE_OFFSET = 37
MAX_PLAYER_COUNT = 4
DEFAULT_COLOR = (255, 255, 255)

class Settings():
	def __init__(self, screen, screen_size: tuple):
		self.screen = screen
		self.screen_size = screen_size
		msg = "Choose Player Count"
		msg_font = pygame.font.Font(None, 42)
		self.msg_text = msg_font.render(msg , True, DEFAULT_COLOR)
		self.msg_rect = self.msg_text.get_rect(center=(self.screen_size[0]/2, LINE_OFFSET + OFFSET))
		self._init_player_count_selection_button()

	def _init_player_count_selection_button(self):
		# init dice images
		self.dice_btns = {}
		for i in range(1, MAX_PLAYER_COUNT + 1):
			img = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
			self.dice_btns[i] = (Dice(img, img, i, i-1, MAX_PLAYER_COUNT, self.screen_size))

	def draw(self, surface: pygame.display):
		# Draw Text
		surface.blit(self.msg_text, self.msg_rect)
		# Draw dice buttons and return selected player count from first clicked dice button or 0
		for i in range(1, MAX_PLAYER_COUNT + 1):
			self.dice_btns[i].draw(self.screen)
			if self.dice_btns[i].listen_for_click():
				return i
		return 0