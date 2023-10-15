import pygame
import sys
import math

class Joystick:
    def __init__(self, screen, position, background_radius=50, handle_radius=15, max_distance=40, color=(255, 255, 255)):
        self.screen = screen
        self.position = position
        self.background_radius = background_radius
        self.handle_radius = handle_radius
        self.max_distance = max_distance
        self.color = color
        self.center = self.position
        self.moving = False

    def draw(self):
        # Draw the joystick background
        pygame.draw.circle(self.screen, self.color, self.position, self.background_radius)
        
        # Draw the movable joystick handle
        pygame.draw.circle(self.screen, self.color, self.position, self.handle_radius)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                distance = math.hypot(mouse_x - self.position[0], mouse_y - self.position[1])
                if distance <= self.background_radius:
                    self.moving = True
        elif event.type == pygame.MOUSEMOTION and self.moving:
            mouse_x, mouse_y = event.pos
            dx = mouse_x - self.center[0]
            dy = mouse_y - self.center[1]
            distance = math.hypot(dx, dy)
            if distance > self.max_distance:
                angle = math.atan2(dy, dx)
                new_x = self.center[0] + self.max_distance * math.cos(angle)
                new_y = self.center[1] + self.max_distance * math.sin(angle)
            else:
                new_x, new_y = mouse_x, mouse_y
            self.position = (new_x, new_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.moving = False
                self.position = self.center

class ImageRotator:
    def __init__(self, screen, position, image_path):
        self.screen = screen
        self.position = position
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.angle = 0  # Initial angle

    def draw(self):
        # Create a rotated image
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = self.position

        # Draw the rotated image
        self.screen.blit(rotated_image, rotated_rect)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Joystick and Rotating Image")

# Create a Joystick instance
joystick = Joystick(screen, (100, 900))

# Create an ImageRotator instance (provide the path to your image)
image_rotator = ImageRotator(screen, (200, 200), 'image_game/blue-tank-0.92.png')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        joystick.update(event)

    screen.fill((0, 0, 0))  # Clear the screen

    # Draw the joystick
    joystick.draw()

    # Update the angle of the rotating image based on joystick position
    dx, dy = joystick.position[0] - joystick.center[0], joystick.position[1] - joystick.center[1]
    angle = math.degrees(math.atan2(dy, dx))
    image_rotator.angle = angle

    # Draw the rotating image
    image_rotator.draw()

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
