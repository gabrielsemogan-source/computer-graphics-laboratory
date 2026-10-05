import pygame
import sys
import math

pygame.init()

# --------------------------------------------------
# WINDOW SETUP
# --------------------------------------------------

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Activity 1 - Tweening, Morphing & Dynamics"
)

clock = pygame.time.Clock()
FPS = 60


# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = (25, 28, 38)
WHITE = (240, 240, 240)
CYAN = (50, 210, 230)
YELLOW = (255, 210, 60)
PURPLE = (170, 100, 230)
GREEN = (80, 220, 130)
GRAY = (100, 105, 115)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def lerp(a, b, t):
    """
    Linear interpolation.

    Formula:
    P(t) = (1 - t) * P_start + t * P_end
    """
    return a + (b - a) * t


def lerp_point(p1, p2, t):
    """
    Linear interpolation between two 2D points.
    """
    x = lerp(p1[0], p2[0], t)
    y = lerp(p1[1], p2[1], t)

    return (x, y)


def ease_in_out(t):
    """
    Smooth ease-in/ease-out motion.
    """
    return t * t * (3 - 2 * t)


# --------------------------------------------------
# TASK 1.1 - TWEENING
# --------------------------------------------------

class Tweening:

    def __init__(self):

        # Multiple keyframe positions
        self.path = [
            (100, 450),
            (220, 180),
            (400, 400),
            (580, 150),
            (720, 420)
        ]

        self.segment = 0
        self.t = 0.0

        # Movement speed
        self.speed = 0.9

    def reset(self):

        self.segment = 0
        self.t = 0.0

    def update(self, dt):

        # Convert speed to time-based movement
        self.t += self.speed * dt

        # Move to next keyframe
        if self.t >= 1.0:

            self.t = 0.0
            self.segment += 1

            # Restart path
            if self.segment >= len(self.path) - 1:
                self.segment = 0

    def get_position(self):

        start = self.path[self.segment]
        end = self.path[self.segment + 1]

        # Smooth interpolation
        smooth_t = ease_in_out(self.t)

        return lerp_point(
            start,
            end,
            smooth_t
        )

    def draw(self):

        # Draw path
        pygame.draw.lines(
            screen,
            GRAY,
            False,
            self.path,
            3
        )

        # Draw keyframe points
        for point in self.path:

            pygame.draw.circle(
                screen,
                WHITE,
                point,
                7
            )

        # Moving sprite
        x, y = self.get_position()

        pygame.draw.circle(
            screen,
            CYAN,
            (int(x), int(y)),
            22
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(x), int(y)),
            22,
            3
        )


# --------------------------------------------------
# TASK 1.2 - POLYGON MORPHING
# --------------------------------------------------

class Morphing:

    def __init__(self):

        # Triangle represented using 4 points.
        #
        # The middle point is duplicated along
        # one edge so both shapes have 4 vertices.

        self.triangle = [
            (400, 120),
            (400, 120),
            (250, 400),
            (550, 400)
        ]

        # Target quadrilateral / rectangle-like shape
        self.rectangle = [
            (280, 180),
            (520, 180),
            (520, 400),
            (280, 400)
        ]

        self.t = 0.0
        self.direction = 1

        self.speed = 0.8

    def reset(self):

        self.t = 0.0
        self.direction = 1

    def update(self, dt):

        self.t += self.direction * self.speed * dt

        # Reverse direction at endpoints
        if self.t >= 1.0:

            self.t = 1.0
            self.direction = -1

        elif self.t <= 0.0:

            self.t = 0.0
            self.direction = 1

    def get_polygon(self):

        smooth_t = ease_in_out(self.t)

        polygon = []

        # Interpolate each matching vertex
        for start, end in zip(
            self.triangle,
            self.rectangle
        ):

            point = lerp_point(
                start,
                end,
                smooth_t
            )

            polygon.append(point)

        return polygon

    def draw(self):

        polygon = self.get_polygon()

        # Fill polygon
        pygame.draw.polygon(
            screen,
            PURPLE,
            polygon
        )

        # Polygon outline
        pygame.draw.polygon(
            screen,
            WHITE,
            polygon,
            4
        )

        # Draw vertices
        for point in polygon:

            pygame.draw.circle(
                screen,
                YELLOW,
                (int(point[0]), int(point[1])),
                6
            )


# --------------------------------------------------
# TASK 1.3 - BOUNCING DYNAMICS
# --------------------------------------------------

class BouncingBall:

    def __init__(self):

        self.x = 150.0
        self.y = 100.0

        self.radius = 25

        # Horizontal velocity
        self.velocity_x = 170.0

        # Vertical velocity
        self.velocity_y = 0.0

        # Gravity
        self.gravity = 900.0

        # Energy retained after collision
        self.restitution = 0.78

        # Floor
        self.floor_y = 500

    def reset(self):

        self.x = 150.0
        self.y = 100.0

        self.velocity_x = 170.0
        self.velocity_y = 0.0

    def update(self, dt):

        # ------------------------------------------
        # KINEMATICS
        #
        # v = v + g * dt
        # y = y + v * dt
        # ------------------------------------------

        self.velocity_y += self.gravity * dt

        self.y += self.velocity_y * dt

        self.x += self.velocity_x * dt

        # ------------------------------------------
        # FLOOR COLLISION
        # ------------------------------------------

        if self.y + self.radius >= self.floor_y:

            self.y = self.floor_y - self.radius

            # v_rebound = -e * v_impact
            self.velocity_y = (
                -self.velocity_y *
                self.restitution
            )

        # ------------------------------------------
        # WALL COLLISIONS
        # ------------------------------------------

        if self.x - self.radius <= 0:

            self.x = self.radius
            self.velocity_x *= -1

        if self.x + self.radius >= WIDTH:

            self.x = WIDTH - self.radius
            self.velocity_x *= -1

    def draw(self):

        # Floor
        pygame.draw.line(
            screen,
            WHITE,
            (0, self.floor_y),
            (WIDTH, self.floor_y),
            4
        )

        # Ball
        pygame.draw.circle(
            screen,
            GREEN,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius,
            3
        )


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

tween = Tweening()
morph = Morphing()
ball = BouncingBall()

mode = 1

running = True

while running:

    # Delta time
    dt = clock.tick(FPS) / 1000.0

    # ----------------------------------------------
    # EVENTS
    # ----------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # Tweening
            if event.key == pygame.K_1:

                mode = 1
                tween.reset()

            # Morphing
            elif event.key == pygame.K_2:

                mode = 2
                morph.reset()

            # Dynamics
            elif event.key == pygame.K_3:

                mode = 3
                ball.reset()

            # Reset
            elif event.key == pygame.K_r:

                if mode == 1:
                    tween.reset()

                elif mode == 2:
                    morph.reset()

                elif mode == 3:
                    ball.reset()

            # Exit
            elif event.key == pygame.K_ESCAPE:

                running = False

    # ----------------------------------------------
    # UPDATE
    # ----------------------------------------------

    if mode == 1:

        tween.update(dt)

    elif mode == 2:

        morph.update(dt)

    elif mode == 3:

        ball.update(dt)

    # ----------------------------------------------
    # DRAW
    # ----------------------------------------------

    screen.fill(BACKGROUND)

    if mode == 1:

        tween.draw()

    elif mode == 2:

        morph.draw()

    elif mode == 3:

        ball.draw()

    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    pygame.display.flip()


pygame.quit()
sys.exit()