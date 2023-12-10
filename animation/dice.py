import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = ( 
    (-1, 1, -1), # 0: left top near
    (1, 1, -1), # 1: right top near
    (1, -1, -1), # 2: right down near
    (-1, -1, -1), # 3: left down near
    (-1, 1, 1), # 4: left top far
    (1, 1, 1), # 5: right top far
    (1, -1, 1), # 6: right down far
    (-1, -1, 1), # 7: left down far
)

surfaces = (
    (0, 1, 2, 3),
    (1, 5, 6, 2),
    (4, 5, 6, 7),
    (4, 0, 3, 7),
    (4, 5, 1, 0),
    (7, 6, 2, 3)
)

# note: y inverted
textureCoordinates = [
    [[0.25, 0.66], [0.25, 0.33], [0.00, 0.33], [0.00, 0.66]], # six
    [[0.25, 0.66], [0.50, 0.66], [0.50, 0.33], [0.25, 0.33]], # four
    [[0.50, 0.66], [0.75, 0.66], [0.75, 0.33], [0.50, 0.33]], # one
    [[0.75, 0.66], [1.00, 0.66], [1.00, 0.33], [0.75, 0.33]], # three
    [[0.50, 0.33], [0.75, 0.33], [0.75, 0.00], [0.50, 0.00]], # two
    [[0.50, 1.00], [0.75, 1.00], [0.75, 0.66], [0.50, 0.66]], # five
]

rotationValues = [
    [0, 0], # one
    [90, 0], # two
    [0, 90], # three
    [0, -90], # four
    [-90, 0], # five
    [180, 90] # six # TODO special case z value instead of y
]

# End positions:
# glRotate(0, 0, 0, 0) # 1
# glRotate(90, 1, 0, 0) # 2
# glRotate(90, 0, 1, 0) # 3
# glRotate(-90, 0, 1, 0) # 4
# glRotate(-90, 1, 0, 0) # 5
# glRotate(90, 0, 0, 1) # 6
# glRotate(180, 1, 0, 0) # 6

def draw():
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        for j, vertex in enumerate(surface):            
            glTexCoord2fv(textureCoordinates[i][j])
            glVertex3fv(verticies[vertex])
    glEnd()
    glDisable(GL_TEXTURE_2D)

def init():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # camera setup
    gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)

def load_texture():
    image = pygame.image.load("dice_texture.jpg")
    datas = pygame.image.tobytes(image, 'RGBA')
    texID = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, datas)

    # use bilinear interpolation
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # only render what is in front
    glEnable(GL_DEPTH_TEST)

def main():
    init()
    load_texture()

    x_angle = -270
    y_angle = 360

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        if x_angle != 90:
            x_angle += 10

        if y_angle != 0:
            y_angle -= 10

        glPushMatrix()
        glRotate(y_angle % 360, 0, 1, 0)
        glRotate(x_angle % 360, 1, 0, 0)
        draw()
        glPopMatrix()        

        pygame.display.flip()

        # Waste time so that frame rate becomes 60 fps
        pygame.time.Clock().tick(60)

main()