import pygame
import math
import sys

pygame.init()

# ==========================================================
# WINDOW
# ==========================================================

WIDTH = 900
HEIGHT = 650
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Activity 4 - 3D Projection Engine"
)

clock = pygame.time.Clock()

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = (18, 22, 30)
WHITE = (240, 240, 240)
CYAN = (60, 210, 230)
YELLOW = (255, 210, 60)
GRAY = (100, 105, 115)

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 24)


# ==========================================================
# 3D CUBE
# ==========================================================

cube_vertices = [
    [-100, -100, -100],
    [100, -100, -100],
    [100, 100, -100],
    [-100, 100, -100],

    [-100, -100, 100],
    [100, -100, 100],
    [100, 100, 100],
    [-100, 100, 100]
]

cube_edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),

    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),

    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]


# ==========================================================
# ROTATION MATRICES
# ==========================================================

def rotate_x(point, angle):

    x, y, z = point

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    new_y = y * cos_a - z * sin_a
    new_z = y * sin_a + z * cos_a

    return [x, new_y, new_z]


def rotate_y(point, angle):

    x, y, z = point

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    new_x = x * cos_a + z * sin_a
    new_z = -x * sin_a + z * cos_a

    return [new_x, y, new_z]


def rotate_z(point, angle):

    x, y, z = point

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a

    return [new_x, new_y, z]


# ==========================================================
# PROJECTION 1 - ORTHOGRAPHIC
# ==========================================================

def project_orthographic(x, y, z):

    screen_x = x + WIDTH // 2
    screen_y = y + HEIGHT // 2

    return int(screen_x), int(screen_y)


# ==========================================================
# PROJECTION 2 & 3 - OBLIQUE
# ==========================================================

def project_oblique(
    x,
    y,
    z,
    mode
):

    if mode == "cavalier":

        # Full depth
        L1 = 1.0

        # 45 degree receding direction
        phi = math.radians(45)

    else:

        # Half depth
        L1 = 0.5

        # Cabinet angle
        phi = math.radians(63.4)

    screen_x = (
        x +
        z * L1 * math.cos(phi)
    )

    screen_y = (
        y +
        z * L1 * math.sin(phi)
    )

    return (
        int(screen_x + WIDTH // 2),
        int(screen_y + HEIGHT // 2)
    )


# ==========================================================
# PROJECTION 4 - PERSPECTIVE
# ==========================================================

def project_perspective(
    x,
    y,
    z
):

    D = 500

    distance = z + D

    if distance <= 1:

        distance = 1

    screen_x = (
        x * D
    ) / distance

    screen_y = (
        y * D
    ) / distance

    return (
        int(screen_x + WIDTH // 2),
        int(screen_y + HEIGHT // 2)
    )


# ==========================================================
# TRANSFORM VERTICES
# ==========================================================

def transform_vertices():

    transformed = []

    for vertex in cube_vertices:

        point = vertex[:]

        # X rotation
        point = rotate_x(
            point,
            rotation_x
        )

        # Y rotation
        point = rotate_y(
            point,
            rotation_y
        )

        # Z rotation
        point = rotate_z(
            point,
            rotation_z
        )

        transformed.append(point)

    return transformed


# ==========================================================
# PROJECT VERTICES
# ==========================================================

def project_vertices(vertices):

    projected = []

    for x, y, z in vertices:

        if projection_mode == 1:

            point = project_orthographic(
                x, y, z
            )

        elif projection_mode == 2:

            point = project_oblique(
                x,
                y,
                z,
                "cavalier"
            )

        elif projection_mode == 3:

            point = project_oblique(
                x,
                y,
                z,
                "cabinet"
            )

        else:

            point = project_perspective(
                x,
                y,
                z
            )

        projected.append(point)

    return projected


# ==========================================================
# DRAW CUBE
# ==========================================================

def draw_cube():

    transformed = transform_vertices()

    projected = project_vertices(
        transformed
    )

    # Draw edges
    for start, end in cube_edges:

        pygame.draw.line(
            screen,
            CYAN,
            projected[start],
            projected[end],
            3
        )

    # Draw vertices
    for point in projected:

        pygame.draw.circle(
            screen,
            YELLOW,
            point,
            6
        )


# ==========================================================
# UI
# ==========================================================

def draw_ui():

    names = {
        1: "Orthographic",
        2: "Cavalier Oblique",
        3: "Cabinet Oblique",
        4: "Perspective"
    }

    title = font.render(
        "Projection: " + names[projection_mode],
        True,
        WHITE
    )

    controls = small_font.render(
        "1-4: Projection   W/S: X   A/D: Y   Q/E: Z",
        True,
        GRAY
    )

    reset_text = small_font.render(
        "R: Reset Rotation   ESC: Exit",
        True,
        GRAY
    )

    screen.blit(
        title,
        (20, 20)
    )

    screen.blit(
        controls,
        (20, 52)
    )

    screen.blit(
        reset_text,
        (20, 78)
    )


# ==========================================================
# INITIAL ROTATION
# ==========================================================

rotation_x = 0.0
rotation_y = 0.0
rotation_z = 0.0

rotation_speed = 0.025

projection_mode = 1


# ==========================================================
# MAIN GAME LOOP
# ==========================================================

running = True

while running:

    clock.tick(FPS)

    # ------------------------------------------------------
    # INPUT
    # ------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # Projection switching
            if event.key == pygame.K_1:
                projection_mode = 1

            elif event.key == pygame.K_2:
                projection_mode = 2

            elif event.key == pygame.K_3:
                projection_mode = 3

            elif event.key == pygame.K_4:
                projection_mode = 4

            # Reset
            elif event.key == pygame.K_r:

                rotation_x = 0
                rotation_y = 0
                rotation_z = 0

            # Exit
            elif event.key == pygame.K_ESCAPE:

                running = False

    # ------------------------------------------------------
    # CONTINUOUS ROTATION INPUT
    # ------------------------------------------------------

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        rotation_x -= rotation_speed

    if keys[pygame.K_s]:
        rotation_x += rotation_speed

    if keys[pygame.K_a]:
        rotation_y -= rotation_speed

    if keys[pygame.K_d]:
        rotation_y += rotation_speed

    if keys[pygame.K_q]:
        rotation_z -= rotation_speed

    if keys[pygame.K_e]:
        rotation_z += rotation_speed

    # ------------------------------------------------------
    # RENDER
    # ------------------------------------------------------

    screen.fill(BACKGROUND)

    draw_cube()

    draw_ui()

    pygame.display.flip()


# ==========================================================
# EXIT
# ==========================================================

pygame.quit()
sys.exit()