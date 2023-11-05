import pygame

from src import Game

PLAYER_NAMES = ["Player 1", "Player 2"]
SCREEN_SIZE = (1280, 720)
CAPTION = "1 - 12"

def main():
	# init game
	game_instance = Game(SCREEN_SIZE, PLAYER_NAMES, CAPTION)

	# game loop
	run = True
	while run:
		game_instance.handle_buttons()
		game_instance.handle_game_play()
		game_instance.show_game_info()

		# event handler
		for event in pygame.event.get():
			# quit game (press X or End Game Button)
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

main()