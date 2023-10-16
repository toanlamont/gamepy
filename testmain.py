import pygame
import sys
import math


class bullet():
    def __init__(self, x, y, radius, color, angle) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = angle
        self.color = color
        self.speed = 20

    def draw_bullet(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Joystick:
    def __init__(self, screen, position, background_radius=50, handle_radius=20, max_distance=40, color=(255, 255, 255)):
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
        pygame.draw.circle(self.screen, (255,0,0), self.center, self.background_radius)
        
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

class Tank():
    def __init__(self, screen, position, image_path):
        self.screen = screen
        self.position = position
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.angle = 0  # Initial angle

    def draw(self):
        # Create a rotated image
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = self.position
        rotated_image.set_colorkey((0,0,0,0))

        # Draw the rotated image
        self.screen.blit(rotated_image, rotated_rect)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Joystick and Rotating Image")

# Create a Joystick instance
joystick = Joystick(screen, (900, 900))
joystick2 = Joystick(screen, (200, 900))


# Create an ImageRotator instance (provide the path to your image)
tank = Tank(screen, [500, 500], 'image_game/blue-tank-0.92.png')

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        joystick.update(event)
        joystick2.update(event)

    screen.fill((128, 0, 128))  # Clear the screen

    # Draw the joystick
    joystick.draw()
    joystick2.draw()

    # Update the angle of the rotating image based on joystick position
    dx, dy = joystick.position[0] - joystick.center[0], joystick.position[1] - joystick.center[1]
    angle = math.degrees(math.atan2(dy, dx))
    tank.angle = angle
    if 

    dx2, dy2 = joystick2.position[0] - joystick2.center[0], joystick2.position[1] - joystick2.center[1]
    angle2 = math.atan2(dy2, dx2)
    new_x = joystick2.max_distance * math.cos(angle2)
    new_y = joystick2.max_distance * math.sin(angle2)
    if int(new_x) == 40:
        new_x = 0 
    if joystick2.moving:
        tank.position[0] += new_x
        tank.position[1] += new_y
    # image_rotator.position[0] += joystick2.center[0] + joystick2.max_distance * math.cos(angle)
    # image_rotator.position[1] += joystick2.center[1] + joystick2.max_distance * math.sin(angle)

    # Draw the rotating image
    tank.draw()

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
