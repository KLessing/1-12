import pygame

X_OFFSET = 0
Y_OFFSET = 0
IMG_WIDTH = 240
IMG_HEIGHT = 240
SCREEN = ((1920, 1080))
X_MAX = 15 # (zero indexed but moduloed)
Y_MAX = 6

x = X_MAX
y = 0

surface = pygame.display.set_mode(SCREEN)
sprite = pygame.image.load("sprite_sheet.png").convert_alpha()
mid = (SCREEN[0]/2 - IMG_WIDTH / 2, SCREEN[1]/2 - IMG_HEIGHT / 2)
clock = pygame.time.Clock()

#game loop
run = True
while run:
    if x < X_MAX:
        x += 1

    # reset view
    surface.fill((0, 0, 0, 0))

    rect = pygame.Rect(IMG_WIDTH * x, IMG_HEIGHT * y, IMG_WIDTH, IMG_HEIGHT)
    surface.blit(sprite, mid, rect)

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