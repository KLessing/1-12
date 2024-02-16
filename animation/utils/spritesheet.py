# This class handles sprite sheets

import pygame

SPRITE_WIDTH = 240
SPRITE_HEIGHT = 240

IMG_WIDTH = 100
IMG_HEIGHT = 100

X_MAX = 15
Y_MAX = 6

class SpriteSheet:

    def __init__(self):
        self.sheet = pygame.image.load("../img/sprite_sheet_green.png").convert_alpha()

    def get_dice(self, number: int):
        rect = pygame.Rect(SPRITE_WIDTH * X_MAX, SPRITE_HEIGHT * number, SPRITE_WIDTH, SPRITE_HEIGHT)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return pygame.transform.scale(image, (IMG_WIDTH, IMG_HEIGHT))

    def get_roll(self):
        pass
