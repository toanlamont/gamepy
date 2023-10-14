import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
TANK_SPEED = 5
BULLET_SPEED = 10
BULLET_COOLDOWN = 30  # Cooldown in frames

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")

# Tank properties
tank_width, tank_height = 50, 50
tank_color = (0, 128, 255)
tank_x, tank_y = (WIDTH - tank_width) // 2, HEIGHT - tank_height

# Bullet properties
bullet_width, bullet_height = 10, 10
bullet_color = (255, 0, 0)
bullets = []
bullet_cooldown = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys pressed by the player
    keys = pygame.key.get_pressed()

    # Adjust tank position based on keys
    if keys[pygame.K_LEFT] and tank_x > 0:
        tank_x -= TANK_SPEED
    if keys[pygame.K_RIGHT] and tank_x < WIDTH - tank_width:
        tank_x += TANK_SPEED

    # Shoot bullets
    if keys[pygame.K_SPACE] and bullet_cooldown <= 0:
        bullet_x = tank_x + (tank_width - bullet_width) / 2
        bullet_y = tank_y
        bullets.append([bullet_x, bullet_y])
        bullet_cooldown = BULLET_COOLDOWN

    # Update bullet positions
    for bullet in bullets:
        bullet[1] -= BULLET_SPEED

    # Remove out-of-screen bullets
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Decrease bullet cooldown
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # Draw everything
    screen.fill(WHITE)

    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))  

    pygame.draw.rect(screen, tank_color, (tank_x, tank_y, tank_width, tank_height))
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
