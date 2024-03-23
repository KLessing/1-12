import random
import time
import utils.globals as globals

from utils.spritesheet import SpriteSheet
from .animated_dice import AnimatedDice as Dice
from .draw_only_dice import DrawOnlyDice

OFFSET = 25
DRAW_ONLY_OFFSET = 115

class DiceController():
	def __init__(self):
		sprite_sheet = SpriteSheet()
        # init empty dice instances
		self.current_dice = []
		self.used_dice = []
		# init dice images
		self.dice_imgs = {}
		self.selected_dice_img = {}
		for i in range(1, globals.MAX_DICE_COUNT + 1):
			self.dice_imgs[i] = sprite_sheet.get_roll_imgs(i)
			self.selected_dice_img[i] = sprite_sheet.get_dice_img(i, True)

	def __get_used_dice_values(self):
		return [dice.value for dice in self.used_dice]

	def __get_all_selected_dice_values(self):
		res = self.get_selected_current_dice_values() + self.__get_used_dice_values()
		return sorted(res, reverse=True)
	
	def get_selected_current_dice_values(self):
		return [dice.value for dice in self.current_dice if dice.clicked]

	def get_current_dice(self):
		return self.current_dice
	
	def get_used_dice(self):
		return self.used_dice
	
	def clear_used_dice(self):
		self.used_dice.clear()

	def get_used_dice_count(self):
		return len(self.used_dice)

	# roll the new current dice and start animation
	def set_current_dice(self, screen_size):
		count = globals.MAX_DICE_COUNT - len(self.used_dice)
		self.current_dice.clear()
		# Seed with current time to microseconds precision
		random.seed(int(time.time() * 1000000))
		for i in range(0, count):
			# roll dice (1-6)
			rdm = random.randrange(1, globals.MAX_DICE_COUNT + 1)
			delay = random.randrange(5, 10)
			self.current_dice.append(Dice(self.dice_imgs[rdm], self.selected_dice_img[rdm], rdm, self.get_mid_pos(i, count, screen_size, globals.IMG_SIZE), delay))

	def set_used_dice(self):
		selected_dice_values = self.__get_all_selected_dice_values()
		self.used_dice.clear()
		width = globals.IMG_SIZE * 0.5
		for index, value in enumerate(selected_dice_values):
			self.used_dice.append(DrawOnlyDice(self.selected_dice_img[value], self.__get_top_pos(index, width), value, width))

	# calc dice pos dynamically in screen mid according to dice index and count of all dice
	def get_mid_pos(self, index: int, count: int, screen_size: tuple, width: int) -> tuple:
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

	# calc pos for two rows in top left corner (max 4)
	def __get_top_pos(self, index: int, width: int) -> tuple:
		y = DRAW_ONLY_OFFSET
		if index >= 2:
			y += width + OFFSET * 2
			index -= 2
		return (index * width + (index + 1) * OFFSET * 2, y)