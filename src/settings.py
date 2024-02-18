import pygame

from utils.spritesheet import SpriteSheet
from .draw_only_dice import DrawOnlyDice
from .dice_controller import DiceController

OFFSET = 15
LINE_OFFSET = 37
MAX_PLAYER_COUNT = 4
DEFAULT_COLOR = (255, 255, 255)

class Settings():
	def __init__(self, screen, screen_size: tuple):
		self.sprite = SpriteSheet()
		self.dice_controller = DiceController()
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
			img = self.sprite.get_dice_img(i)
			width = img.get_width()
			pos = self.dice_controller.get_mid_pos(i-1, MAX_PLAYER_COUNT, self.screen_size, width)
			self.dice_btns[i] = (DrawOnlyDice(img, pos, i, width))

	def draw(self, surface: pygame.display):
		# Draw Text
		surface.blit(self.msg_text, self.msg_rect)
		# Draw dice buttons and return selected player count from first clicked dice button or 0
		for i in range(1, MAX_PLAYER_COUNT + 1):
			self.dice_btns[i].draw(self.screen)
			if self.dice_btns[i].listen_for_click():
				return i
		return 0