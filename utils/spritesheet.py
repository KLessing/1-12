# This class handles sprite sheets

import pygame
import utils.globals as globals

SPRITE_WIDTH = 240
SPRITE_HEIGHT = 240

X_MAX = 15 # (0 - 15)

class SpriteSheet:

    def __init__(self):
        # convert alpha to keep transparency (while optimizing blitting)
        self.sheet_green = pygame.image.load("img/sprite_sheet_green.png").convert_alpha()
        self.sheet_red = pygame.image.load("img/sprite_sheet_red.png").convert_alpha()

    def get_dice_img(self, number: int, clicked: bool = False, x : int = X_MAX):
        if number <= 0 or number > globals.MAX_DICE_COUNT:
            return
        
        number -= 1
        rect = pygame.Rect(SPRITE_WIDTH * x, SPRITE_HEIGHT * number, SPRITE_WIDTH, SPRITE_HEIGHT)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)

        if clicked:
            sheet = self.sheet_red
        else:
            sheet = self.sheet_green

        image.blit(sheet, (0, 0), rect)


        return pygame.transform.scale(image, (globals.IMG_SIZE, globals.IMG_SIZE))

    def get_roll_imgs(self, number: int):
        return [self.get_dice_img(number, False, x) for x in range(X_MAX + 1)]
