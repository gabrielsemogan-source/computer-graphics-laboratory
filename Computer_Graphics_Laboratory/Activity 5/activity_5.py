# Activity 5: Hardware Graphics Pipeline & Shading using PyOpenGL

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

pygame.init()

display = (800, 600)

pygame.display.set_mode(
    display,
    DOUBLEBUF | OPENGL
)

pygame.display.set_caption(
    "Activity 5: Hardware Graphics Pipeline with PyOpenGL"
)


# --------------------------------------------------
# PERSPECTIVE CAMERA SETUP
# --------------------------------------------------

glMatrixMode(GL_PROJECTION)
glLoadIdentity()

gluPerspective(
    45,
    display[0] / display[1],
    0.1,
    50.0
)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

glTranslatef(0.0, 0.0, -7.0)


# --------------------------------------------------
# DEPTH BUFFER
# --------------------------------------------------

glEnable(GL_DEPTH_TEST)


# --------------------------------------------------
# ALPHA BLENDING
# --------------------------------------------------

glEnable(GL_BLEND)

glBlendFunc(
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA
)


# --------------------------------------------------
# CUBE DATA
# --------------------------------------------------

vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),

    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
]

colors = [
    (1, 0, 0),       # Red
    (0, 1, 0),       # Green
    (0, 0, 1),       # Blue
    (1, 1, 0),       # Yellow
    (1, 0, 1),       # Magenta
    (0, 1, 1),       # Cyan
    (1, 1, 1),       # White
    (0.5, 0.5, 0.5)  # Gray
]

surfaces = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
]


# --------------------------------------------------
# TASK 5.2
# COLORED CUBE
# --------------------------------------------------

def draw_colored_cube():

    glBegin(GL_QUADS)

    for surface in surfaces:

        for vertex_index in surface:

            glColor3fv(colors[vertex_index])

            glVertex3fv(vertices[vertex_index])

    glEnd()


# --------------------------------------------------
# ARTICULATED ARM
# TASK 5.3
# --------------------------------------------------

def draw_arm():

    # Upper arm
    glPushMatrix()

    glTranslatef(-1.5, 0.5, 0.0)

    glRotatef(
        pygame.time.get_ticks() * 0.05,
        0,
        0,
        1
    )

    glScalef(0.5, 1.5, 0.5)

    glColor3f(1.0, 0.5, 0.0)

    draw_colored_cube()

    glPopMatrix()


    # Lower arm
    glPushMatrix()

    glTranslatef(
        -1.5,
        -1.2,
        0.0
    )

    glRotatef(
        pygame.time.get_ticks() * 0.08,
        0,
        0,
        1
    )

    glScalef(0.4, 1.0, 0.4)

    glColor3f(0.2, 0.8, 1.0)

    draw_colored_cube()

    glPopMatrix()


# --------------------------------------------------
# TASK 5.4
# TRANSPARENT POLYGONS
# --------------------------------------------------

def draw_transparent_polygons():

    # First transparent polygon
    glPushMatrix()

    glTranslatef(1.3, 0.5, 0.0)

    glRotatef(
        pygame.time.get_ticks() * 0.05,
        0,
        1,
        0
    )

    glColor4f(
        1.0,
        0.0,
        0.0,
        0.5
    )

    glBegin(GL_QUADS)

    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)

    glEnd()

    glPopMatrix()


    # Second transparent polygon
    glPushMatrix()

    glTranslatef(
        1.3,
        0.5,
        -0.5
    )

    glRotatef(
        pygame.time.get_ticks() * -0.04,
        0,
        1,
        0
    )

    glColor4f(
        0.0,
        0.0,
        1.0,
        0.5
    )

    glBegin(GL_QUADS)

    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)

    glEnd()

    glPopMatrix()


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

clock = pygame.time.Clock()

rotation = 0.0

running = True

while running:

    # ----------------------------------------------
    # EVENTS
    # ----------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False


    # ----------------------------------------------
    # UPDATE ROTATION
    # ----------------------------------------------

    rotation += 1.0


    # ----------------------------------------------
    # CLEAR COLOR + DEPTH BUFFER
    # ----------------------------------------------

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )


    # ----------------------------------------------
    # RESET MODELVIEW
    # ----------------------------------------------

    glLoadIdentity()

    glTranslatef(
        0.0,
        0.0,
        -7.0
    )


    # ----------------------------------------------
    # MAIN ROTATING CUBE
    # TASK 5.2 + 5.3
    # ----------------------------------------------

    glPushMatrix()

    glRotatef(
        rotation,
        1,
        1,
        0
    )

    glRotatef(
        rotation * 0.5,
        0,
        1,
        1
    )

    glScalef(
        1.2,
        1.2,
        1.2
    )

    draw_colored_cube()

    glPopMatrix()


    # ----------------------------------------------
    # ARTICULATED ARM
    # ----------------------------------------------

    draw_arm()


    # ----------------------------------------------
    # TRANSPARENT OBJECTS
    # ----------------------------------------------

    draw_transparent_polygons()


    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    pygame.display.flip()

    clock.tick(60)


# --------------------------------------------------
# EXIT
# --------------------------------------------------

pygame.quit()
sys.exit()