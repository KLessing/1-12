import pygame
import random
import utils.globals as globals

from utils.spritesheet import SpriteSheet
from dice import Dice

OFFSET = 30

class DiceController():
	def __init__(self):
		sprite_sheet = SpriteSheet()

		# init dice images
		self.dice_img = {}
		self.selected_dice_img = {}
		for i in range(1, globals.MAX_DICE_COUNT + 1):
			self.dice_img[i] = sprite_sheet.get_dice_img(i)
			self.selected_dice_img[i] = sprite_sheet.get_dice_img(i, True)

		# init empty dice instances
		self.current_dice = []
		self.used_dice = []
		# needed for multiple possible combinations for first move (4 + 4 = 4 or 8) 
		self.validated_combinations = set()

	def roll_dice(self, count: int, screen_size):
		dice = []
		for i in range(0, count):
			# roll dice (1-6)
			rdm = random.randrange(1, globals.MAX_DICE_COUNT + 1)
			dice.append(Dice(self.dice_img[rdm], self.selected_dice_img[rdm], rdm, self.get_pos(i, count, screen_size, globals.IMG_SIZE)))
		# TODO start animation
		return dice

	# calc dice pos dynamically in screen mid according to dice index and count of all dice
	def get_pos(self, index: int, count: int, screen_size: tuple, width: int) -> tuple:
		# separate all dice into two rows
		# round down to whole number with //
		separator = count // 2 
		height_mid = screen_size[1] // 2
		
		if count == 1:
			# single dice
			y = height_mid - (width // 2)
			col_index = 0 # the index in the row
			col_count = 1 # how many columns (dice) are in the row
		elif index < separator:
			# top row
			y = height_mid - width - (OFFSET // 2)
			col_index = index
			col_count = separator
		else:
			# bottom row
			y = height_mid + (OFFSET // 2)
			col_index = index - separator
			col_count = count - separator

		dice_row_width = col_count * width + (col_count - 1) * OFFSET
		dice_row_pos = (screen_size[0] // 2) - (dice_row_width // 2)
		x = col_index * (width + OFFSET) + dice_row_pos
			
		return (x, y)	