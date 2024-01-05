import pygame

X_OFFSET = 0
Y_OFFSET = 10
IMG_WIDTH = 234
IMG_HEIGHT = 240
SCREEN = ((1980, 1080))
X_MAX = 15 # (zero indexed)
Y_MAX = 6 # (zero indexed)

x = 0
y = 0

surface = pygame.display.set_mode(SCREEN)
sprite = pygame.image.load("dice_spritesheet.png").convert_alpha()
mid = (SCREEN[0]/2 - IMG_WIDTH / 2, SCREEN[1]/2 - IMG_HEIGHT / 2)
rect = pygame.Rect(X_OFFSET * x + IMG_WIDTH * x, Y_OFFSET * y + IMG_HEIGHT * y, IMG_WIDTH, IMG_HEIGHT)

#game loop
run = True
while run:
	
    surface.blit(sprite, mid, rect)

    #event handler
    for event in pygame.event.get():
        pass
        #quit game (press X)
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()