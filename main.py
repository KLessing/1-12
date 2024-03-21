#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import pygame

from src import Game

SCREEN_SIZE = (1440, 900) # 16:10
# SCREEN_SIZE = (1280, 720) # 16:9
# SCREEN_SIZE = (1920, 1080) # 16:9

clock = pygame.time.Clock()

async def main():
	# init game
	game_instance = Game(SCREEN_SIZE)

	# game loop
	run = True
	while run:
		game_instance.handle_game_state()

		# event handler
		for event in pygame.event.get():
			# quit game (press X or End Game Button)
			if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
				run = False

		clock.tick(60)
		pygame.display.update()
		await asyncio.sleep(0)

	pygame.quit()

asyncio.run(main())
