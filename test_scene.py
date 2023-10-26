import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Explosion Animation Example")

# Load explosion frames (replace with your own images)
frame1 = pygame.transform.scale(pygame.image.load('image_game/explode1.png'), (50, 50))
frame2 = pygame.transform.scale(pygame.image.load('image_game/explode2.png'), (50, 50))
frame3 = pygame.transform.scale(pygame.image.load('image_game/explode3.png'), (50, 50))
frame4 = pygame.transform.scale(pygame.image.load('image_game/explode4.png'), (50, 50))


explosion_frames = [frame1, frame2, frame3, frame4]

# Create an Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, x, y):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_delay = 10

    def update(self):
        self.frame_delay -= 1
        if self.frame_delay <= 0:
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
                self.frame_delay = 5
            else:
                self.kill()

explosions = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        explosion = Explosion(explosion_frames, 100, 100)
        explosions.add(explosion)

    screen.fill(WHITE)

    explosions.update()
    explosions.draw(screen)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
