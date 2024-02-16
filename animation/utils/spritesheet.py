# This class handles sprite sheets

import pygame

SPRITE_WIDTH = 240
SPRITE_HEIGHT = 240

IMG_WIDTH = 100
IMG_HEIGHT = 100

X_MAX = 15 # (0 - 15)
Y_MAX = 6 # (1- 6)

class SpriteSheet:

    def __init__(self):
        self.sheet = pygame.image.load("../img/sprite_sheet_green.png").convert_alpha()

    def get_dice(self, number: int, x : int = X_MAX):
        if number <= 0 or number > Y_MAX:
            return
        
        number -= 1
        rect = pygame.Rect(SPRITE_WIDTH * x, SPRITE_HEIGHT * number, SPRITE_WIDTH, SPRITE_HEIGHT)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return pygame.transform.scale(image, (IMG_WIDTH, IMG_HEIGHT))

    def get_roll(self, number: int):
        return [self.get_dice(number, x) for x in range(X_MAX + 1)]
