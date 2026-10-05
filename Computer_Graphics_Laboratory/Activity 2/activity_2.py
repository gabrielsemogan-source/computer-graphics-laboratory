import pygame
import random
import sys

pygame.init()

# --------------------------------------------------
# WINDOW
# --------------------------------------------------

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 2 - Interactive Collision Arena")

clock = pygame.time.Clock()

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = (20, 24, 32)
WHITE = (240, 240, 240)
GREEN = (60, 220, 130)
RED = (230, 70, 70)
YELLOW = (255, 210, 60)
GRAY = (80, 85, 95)

# --------------------------------------------------
# FONTS
# --------------------------------------------------

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)


# ==================================================
# PLAYER SPRITE
# ==================================================

class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        # Transparent surface
        self.image = pygame.Surface(
            (46, 46),
            pygame.SRCALPHA
        )

        # Draw player
        pygame.draw.circle(
            self.image,
            GREEN,
            (23, 23),
            21
        )

        pygame.draw.circle(
            self.image,
            WHITE,
            (23, 23),
            21,
            3
        )

        # Rect anchor
        self.rect = self.image.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )

        self.speed = 5

    def update(self):

        keys = pygame.key.get_pressed()

        # ------------------------------------------
        # KEYBOARD MOVEMENT
        # ------------------------------------------

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # ------------------------------------------
        # SCREEN BOUNDARY CLAMPING
        # ------------------------------------------

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


# ==================================================
# OBSTACLE SPRITE
# ==================================================

class Obstacle(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        size = random.randint(30, 50)

        self.image = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            self.image,
            RED,
            self.image.get_rect(),
            border_radius=8
        )

        self.rect = self.image.get_rect(
            center=(
                random.randint(60, WIDTH - 60),
                random.randint(80, HEIGHT - 60)
            )
        )

        # Random movement
        self.velocity_x = random.choice([-2, -1, 1, 2])
        self.velocity_y = random.choice([-2, -1, 1, 2])

    def update(self):

        # Move obstacle
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Bounce from walls
        if self.rect.left <= 0:
            self.rect.left = 0
            self.velocity_x *= -1

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.velocity_x *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y *= -1

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y *= -1


# ==================================================
# IMPACT PARTICLE
# ==================================================

class ImpactParticle(pygame.sprite.Sprite):

    def __init__(self, position):

        super().__init__()

        self.size = random.randint(5, 10)

        # SRCALPHA gives transparency
        self.image = pygame.Surface(
            (self.size * 2, self.size * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            self.image,
            (255, 210, 60, 220),
            (self.size, self.size),
            self.size
        )

        self.rect = self.image.get_rect(
            center=position
        )

        self.life = 30

        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)

    def update(self):

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        self.life -= 1

        # Alpha fading
        alpha = max(0, int(255 * self.life / 30))

        self.image.set_alpha(alpha)

        if self.life <= 0:
            self.kill()


# ==================================================
# CREATE SPRITES
# ==================================================

player = Player()

player_group = pygame.sprite.Group()
player_group.add(player)

obstacle_group = pygame.sprite.Group()

for i in range(8):

    obstacle = Obstacle()

    obstacle_group.add(obstacle)


particle_group = pygame.sprite.Group()


# ==================================================
# GAME VARIABLES
# ==================================================

score = 0
health = 100

collision_cooldown = 0


# ==================================================
# MAIN GAME LOOP
# ==================================================

running = True

while running:

    # ------------------------------------------------
    # FPS REGULATION
    # ------------------------------------------------

    dt = clock.tick(FPS)

    # ------------------------------------------------
    # PROCESS INPUT
    # ------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

    # ------------------------------------------------
    # UPDATE GAME STATE
    # ------------------------------------------------

    player_group.update()

    obstacle_group.update()

    particle_group.update()

    # Reduce collision cooldown
    if collision_cooldown > 0:

        collision_cooldown -= 1

    # ------------------------------------------------
    # COLLISION DETECTION
    # ------------------------------------------------

    if collision_cooldown <= 0:

        collided = pygame.sprite.spritecollide(
            player,
            obstacle_group,
            False,
            collided=pygame.sprite.collide_rect
        )

        if collided:

            # Lose health
            health -= 10

            # Increase score
            score += 10

            # Create impact particles
            for i in range(15):

                particle = ImpactParticle(
                    player.rect.center
                )

                particle_group.add(particle)

            # Prevent instant repeated collisions
            collision_cooldown = 30

            # Reset player position
            player.rect.center = (
                WIDTH // 2,
                HEIGHT // 2
            )

    # ------------------------------------------------
    # GAME OVER
    # ------------------------------------------------

    if health <= 0:

        health = 0

    # ------------------------------------------------
    # RENDER
    # ------------------------------------------------

    screen.fill(BACKGROUND)

    # Draw obstacles
    obstacle_group.draw(screen)

    # Draw player
    player_group.draw(screen)

    # Draw particles
    particle_group.draw(screen)

    # ------------------------------------------------
    # HUD
    # ------------------------------------------------

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    health_text = font.render(
        f"Health: {health}",
        True,
        WHITE
    )

    controls_text = small_font.render(
        "Arrow Keys = Move     ESC = Exit",
        True,
        GRAY
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        health_text,
        (20, 55)
    )

    screen.blit(
        controls_text,
        (20, HEIGHT - 35)
    )

    # Game over message
    if health <= 0:

        game_over = font.render(
            "GAME OVER - Restart the program",
            True,
            RED
        )

        screen.blit(
            game_over,
            (
                WIDTH // 2 - game_over.get_width() // 2,
                HEIGHT // 2
            )
        )

    # ------------------------------------------------
    # DISPLAY
    # ------------------------------------------------

    pygame.display.flip()


# ==================================================
# EXIT
# ==================================================

pygame.quit()
sys.exit()