import pygame
import math

# Initialize pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Define a sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0  # Initial angle

    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)

# Load your sprite image
sprite_image = pygame.image.load("image_game/blue-tank-0.92.png")

# Create sprite objects
sprite1 = MySprite(sprite_image, 100, 100)
sprite2 = MySprite(sprite_image, 200, 200)

# Create a sprite group
sprite_group = pygame.sprite.Group()
sprite_group.add(sprite1, sprite2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the sprites
    sprite1.rotate(1)  # Rotate sprite1 by 1 degree per frame
    sprite2.rotate(-1)  # Rotate sprite2 by -1 degree per frame

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the sprites
    sprite_group.draw(screen)

    pygame.display.flip()

pygame.quit()
