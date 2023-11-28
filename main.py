import asyncio
import pygame

from src import Game

SCREEN_SIZE = (1280, 720)

async def main():
	my_clock = pygame.time.Clock()

	# init game
	game_instance = Game(SCREEN_SIZE)

	# game loop
	run = True
	while run:
		game_instance.handle_game_state()

		# event handler
		for event in pygame.event.get():
			# quit game (press X or End Game Button)
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

		await asyncio.sleep(0)

		# Waste time so that frame rate becomes 60 fps
		my_clock.tick(60)

	pygame.quit()

asyncio.run(main())
