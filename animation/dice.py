import pygame

from OpenGL.GL import *

import random

# how fast is the animation
ANIMATION_RATE = 4

VERTICIES = ( 
    (-1, 1, -1), # 0: left top near
    (1, 1, -1), # 1: right top near
    (1, -1, -1), # 2: right down near
    (-1, -1, -1), # 3: left down near
    (-1, 1, 1), # 4: left top far
    (1, 1, 1), # 5: right top far
    (1, -1, 1), # 6: right down far
    (-1, -1, 1), # 7: left down far
)

SURFACES = (
    (0, 1, 2, 3),
    (1, 5, 6, 2),
    (4, 5, 6, 7),
    (4, 0, 3, 7),
    (4, 5, 1, 0),
    (7, 6, 2, 3)
)

# note: y inverted
TEXTURE_COORDINATES = [
    [[0.00, 0.66], [0.25, 0.66], [0.25, 0.33], [0.00, 0.33]], # six
    [[0.25, 0.66], [0.50, 0.66], [0.50, 0.33], [0.25, 0.33]], # four
    [[0.50, 0.66], [0.75, 0.66], [0.75, 0.33], [0.50, 0.33]], # one
    [[0.75, 0.66], [1.00, 0.66], [1.00, 0.33], [0.75, 0.33]], # three
    [[0.50, 0.33], [0.75, 0.33], [0.75, 0.00], [0.50, 0.00]], # two
    [[0.50, 1.00], [0.75, 1.00], [0.75, 0.66], [0.50, 0.66]], # five
]

ROTATION_VALUES = [
    [0, 0], # one
    [90, 0], # two
    [0, 90], # three
    [0, -90], # four
    [-90, 0], # five
    [180, 0] # six
]

class Dice():
    def __init__(self, translation, min_pos, max_pos):
        self.pos = translation
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.roll = 1
        self.remaining_duration = 0
        self.is_selected = False
        self.load_texture()

    def load_texture(self):
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

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        for i, surface in enumerate(SURFACES):
            for j, vertex in enumerate(surface):            
                glTexCoord2fv(TEXTURE_COORDINATES[i][j])
                glVertex3fv(VERTICIES[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    # animate the roll while duration is not 0
    def roll_animation(self):
        if self.remaining_duration >= ANIMATION_RATE:
            self.remaining_duration -= ANIMATION_RATE

        if self.is_selected:
            glColor(255, 0, 0)
        else:
            glColor(255, 255, 255)

        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glScalef(0.25, 0.25, 0.25)
        glRotate(self.remaining_duration + ROTATION_VALUES[self.roll-1][0] % 360, 1, 0, 0) # x
        glRotate(self.remaining_duration + ROTATION_VALUES[self.roll-1][1] % 360, 0, 1, 0) # y
        self.draw()
        glPopMatrix()

    def trigger_animation(self):
        # complete duration
        duration_value = random.randrange(3, 6)
        animation_duration = duration_value * 100

        self.roll = random.randrange(1, 7)

        # remaining duration value
        self.remaining_duration = animation_duration

    def check_selection(self, x, y):
        if (x >= self.min_pos[0] and
            y >= self.min_pos[1] and
            x <= self.max_pos[0] and
            y <= self.max_pos[1]):
            self.select()

    def select(self):
        self.is_selected = not self.is_selected

