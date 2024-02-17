#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from dice_controller import DiceController
from utils.spritesheet import SpriteSheet

IMG_WIDTH = 100
IMG_HEIGHT = 100
SCREEN = (1280, 720)
X_MAX = 15 # (zero indexed but moduloed)
Y_MAX = 6

x = X_MAX
y = 0

surface = pygame.display.set_mode(SCREEN)
background = pygame.image.load('../img/background_1280px.jpg').convert_alpha()
spritesheet = SpriteSheet()
clock = pygame.time.Clock()
mid = (SCREEN[0]/2 - IMG_WIDTH / 2, SCREEN[1]/2 - IMG_HEIGHT / 2)
roll_images = spritesheet.get_roll_imgs(6)

dc = DiceController()
dice = dc.roll_dice(6, SCREEN)

#game loop
run = True
while run:
    # reset view
    surface.blit(background, [0, 0])

    for d in dice:
        d.draw(surface)
        d.listen_for_click()       

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            #quit game (press X)
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # left click 
            x = 0
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            # right click
            y = (y + 1) % Y_MAX

    clock.tick(10)
    pygame.display.update()

pygame.quit()