import asyncio

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from dice import Dice

SCREEN_SIZE = (1280, 720)

def init():
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF|OPENGL)

    # camera setup
    gluPerspective(90, (SCREEN_SIZE[0]/SCREEN_SIZE[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)

async def main():
	init() 
	dice = Dice()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				print("left click")
			if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
				dice.trigger_animation()
		
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		dice.roll_animation()

		pygame.display.flip()

		# Waste time so that frame rate becomes 60 fps
		pygame.time.Clock().tick(60)
		
		await asyncio.sleep(0)
        

asyncio.run(main())
