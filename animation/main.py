import asyncio

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from dice import Dice

SCREEN_SIZE = (1280, 720)

DICE_TRANSLATIONS = [
	(-1, 1, 0),
	(0, 1, 0),
	(1, 1, 0),
	(-1, 0, 0),
	(0, 0, 0),
	(1, 0, 0),
]

DICE_POS = [
	[(325, 170), (450, 290)],
	[(575, 170), (700, 290)],
	[(825, 170), (955, 290)],
	[(325, 420), (450, 545)],
	[(575, 420), (700, 545)],
	[(825, 420), (955, 545)],
]

def init():
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF|OPENGL)

    # camera setup
    gluPerspective(65, (SCREEN_SIZE[0]/SCREEN_SIZE[1]), 0.1, 50.0)
    glTranslatef(0, -0.5, -2.5)

async def main():
	init() 

	dice = []
	for i in range(6):
		dice.append(Dice(DICE_TRANSLATIONS[i], DICE_POS[i][0], DICE_POS[i][1]))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# x button
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				# left click
				x, y = pygame.mouse.get_pos()
				for d in dice:
					d.check_selection(x, y)
			if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
				# right click
				for d in dice:
					d.trigger_animation()
		
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		for d in dice:
			d.roll_animation()

		pygame.display.flip()

		# Waste time so that frame rate becomes 60 fps
		pygame.time.Clock().tick(60)
		
		await asyncio.sleep(0)
        

asyncio.run(main())
