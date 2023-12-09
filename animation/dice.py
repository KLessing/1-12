import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (  
    (-1, 1, 1), # 0: left top near
    (1, 1, 1), # 1: right top near
    (1, -1, 1), # 2: right down near
    (-1, -1, 1), # 3: left down near
    (-1, 1, -1), # 4: left top far
    (1, 1, -1), # 5: right top far
    (1, -1, -1), # 6: right down far
    (-1, -1, -1), # 7: left down far
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 6),
    (5, 4),
    (5, 6),
    (5, 1),
    (7, 4),
    (7, 6),
    (7, 3),
)

surfaces = (
    (0, 1, 2, 3),
    (1, 5, 6, 2),
    (4, 5, 6, 7),
    (4, 0, 3, 7),
    (4, 5, 1, 0),
    (7, 6, 2, 3)
)

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for i, vertex in enumerate(surface):
            x+=1
            glColor3f(1, 1, 1)
            glTexCoord2fv(textureCoordinates[i])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    my_clock = pygame.time.Clock()

    # camera setup
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        #glTranslatef(0.01, 0.01, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()

        # Waste time so that frame rate becomes 60 fps
        my_clock.tick(60)


main()