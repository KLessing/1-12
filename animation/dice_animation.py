import pygame

X_OFFSET = 0
Y_OFFSET = 10
IMG_WIDTH = 234
IMG_HEIGHT = 240
SCREEN = ((1980, 1080))
X_MAX = 16 # (zero indexed but moduloed)
Y_MAX = 7

x = 0
y = 0

surface = pygame.display.set_mode(SCREEN)
sprite = pygame.image.load("dice_spritesheet.png").convert_alpha()
mid = (SCREEN[0]/2 - IMG_WIDTH / 2, SCREEN[1]/2 - IMG_HEIGHT / 2)
clock = pygame.time.Clock()


#game loop
run = True
while run:
    x = (x + 1) % X_MAX

    # reset view
    surface.fill((0, 0, 0, 0))

    rect = pygame.Rect(X_OFFSET * x + IMG_WIDTH * x, Y_OFFSET * y + IMG_HEIGHT * y, IMG_WIDTH, IMG_HEIGHT)
    surface.blit(sprite, mid, rect)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #quit game (press X)
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # left click            
            x = (x + 1) % X_MAX
            print("x =", x)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            # right click
            y = (y + 1) % Y_MAX
            print("y =", y)

    clock.tick(10)
    pygame.display.update()

pygame.quit()