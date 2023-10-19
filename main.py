import pygame
import sys
import math
import os


color_dict = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
    'brown': (139, 69, 19),
    'gray': (128, 128, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'lime': (0, 255, 0),
    'teal': (0, 128, 128),
    'navy': (0, 0, 128),
    'gold': (255, 215, 0),
    'silver': (192, 192, 192),
    'violet': (238, 130, 238),
    'indigo': (75, 0, 130)
}

pygame.init()
# Set up the screen
# win_size = (screen.get_width(), screen.get_height())
win_size = (1920, 1080)

# screen = pygame.display.set_mode((1920, 1080))
# screen = pygame.display.set_mode(win_size, pygame.FULLSCREEN)

# # pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.QUIT,
#                               pygame.FINGERUP, pygame.FINGERDOWN, pygame.KEYDOWN, pygame.KEYUP])
screen = pygame.display.set_mode(win_size)

pygame.display.set_caption("Joystick and Rotating Image")


class bullet():
    def __init__(self, x, y, radius, color, angle=None) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = angle
        self.color = color
        self.speed = 20
        self.angle = angle

    def draw_bullet(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Joystick:
    def __init__(self, screen, position, background_radius=150, handle_radius=100, max_distance=100, color=(255, 255, 255)):
        self.screen = screen
        self.position = position
        self.background_radius = background_radius
        self.handle_radius = handle_radius
        self.max_distance = max_distance
        self.color = color
        self.center = self.position
        self.moving = False
        self.angle = None

    def draw(self):
        # Draw the joystick background
        pygame.draw.circle(self.screen, (255,0,0), self.center, self.background_radius)
        
        # Draw the movable joystick handle
        pygame.draw.circle(self.screen, self.color, self.position, self.handle_radius)

    def update(self, event):
        if event.type == pygame.FINGERDOWN:
            mouse_x, mouse_y = (event.dict['x']* win_size[0], event.dict['y']*win_size[1])
            distance = math.hypot(mouse_x - self.position[0], mouse_y - self.position[1])
            if distance <= self.background_radius:
                self.moving = True
        elif event.type == pygame.FINGERMOTION and self.moving:
            mouse_x, mouse_y = (event.dict['x']* win_size[0], event.dict['y']*win_size[1])
            dx = mouse_x - self.center[0]
            dy = mouse_y - self.center[1]
            distance = math.hypot(dx, dy)
            if distance > self.max_distance:
                angle = math.atan2(dy, dx)
                self.angle = angle
                new_x = self.center[0] + self.max_distance * math.cos(angle)
                new_y = self.center[1] + self.max_distance * math.sin(angle)
            else:
                new_x, new_y = mouse_x, mouse_y
            self.position = (new_x, new_y)
        elif event.type == pygame.FINGERUP:
            self.moving = False
            self.position = self.center

        if event.type == pygame.MOUSEBUTTONDOWN:
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
                self.angle = angle
                new_x = self.center[0] + self.max_distance * math.cos(angle)
                new_y = self.center[1] + self.max_distance * math.sin(angle)
            else:
                new_x, new_y = mouse_x, mouse_y
            self.position = (new_x, new_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.moving = False
            self.position = self.center

class Tank():
    def __init__(self, screen, position, image_path):
        self.screen = screen
        self.position = position
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.angle = 0  # Initial angle
        self.health = 100


    def draw(self):
        self.hitbox = [self.position[0] - 50, self.position[1]- 50, 100, 100]
        # Create a rotated image
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = self.position
        rotated_image.set_colorkey((0,0,0,0))
        pygame.draw.rect(screen, color_dict['gray'], self.hitbox, 2)
        pygame.draw.rect(screen, color_dict['red'], (self.position[0] - 50, self.position[1] - 50, 100, 10))
        pygame.draw.rect(screen, color_dict['navy'], (self.position[0] - 50, self.position[1] - 50, self.health, 10))

        # Draw the rotated image
        self.screen.blit(rotated_image, rotated_rect)

    def hit(self):
        self.health -= 1


class Enemy():
    def __init__(self, screen, position, image_path):
        self.screen = screen
        self.position = position
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.angle = 0  # Initial angle
        self.health = 100
        self.i = 0

    def draw(self):
        # Create a rotated image
        self.hitbox = [self.position[0] - 50, self.position[1]- 50, 100, 100]
        self.image = pygame.transform.scale(self.image, (100, 100))
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = self.position
        rotated_image.set_colorkey((0,0,0,0))
        pygame.draw.rect(screen, color_dict['cyan'], self.hitbox, 2)

        # Draw the rotated image
        self.screen.blit(rotated_image, rotated_rect)
        pygame.draw.rect(screen, color_dict['red'], (self.position[0] - 50, self.position[1] - 50, 100, 10))
        pygame.draw.rect(screen, color_dict['navy'], (self.position[0] - 50, self.position[1] - 50, self.health, 10))

    def hit(self):
        self.i += 1
        self.health -= 1

# Initialize Pygame


# Create a Joystick instance
joystick = Joystick(screen, (1800, 800))
joystick2 = Joystick(screen, (200, 800))
curr_dir = (os.getcwd())


# Create an ImageRotator instance (provide the path to your image)
tank = Tank(screen, [500, 500], f'{curr_dir}/image_game/blue-tank-0.92.png')
enemy = Enemy(screen, [800, 500], f'{curr_dir}/image_game/mothership-0.92.png')
bullets = []
enemies = []

running = True
clock = pygame.time.Clock()

def re_draw_all():
    joystick.draw()
    joystick2.draw()
    tank.draw()
    for ene in enemies:
        ene.draw()

    for b in bullets:
        b.draw_bullet()
clock_count = 0
while running:
    clock.tick(27)
    clock_count += 1
    if clock_count > 27:
        clock_count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        joystick.update(event)
        joystick2.update(event)

    screen.fill((102, 153, 255))  # Clear the screen

    # Update the angle of the rotating image based on joystick position
    dx, dy = joystick.position[0] - joystick.center[0], joystick.position[1] - joystick.center[1]
    angle = math.atan2(dy, dx)
    if joystick.moving:
        tank.angle = angle

    dx2, dy2 = joystick2.position[0] - joystick2.center[0], joystick2.position[1] - joystick2.center[1]
    angle2 = math.atan2(dy2, dx2)

    new_x = 20 * math.cos(angle2)
    new_y = 20 * math.sin(angle2)
    if int(new_x) == 40:
        new_x = 0 
    if joystick2.moving:
        
        tank.position[0] += new_x
        tank.position[1] += new_y

    if joystick.moving and clock_count % 9 == 0:
        bullets.append(bullet(x=tank.position[0] + 100* math.cos(tank.angle), y=tank.position[1] + 100* math.sin(tank.angle), radius=10, color=(255,0,0), angle=tank.angle))

    if len(enemies) == 0:
        enemies.append(Enemy(screen, [800, 500], f'{curr_dir}/image_game/mothership-0.92.png'))

    for ene in enemies:
        
        dx_ene, dy_ene = ene.position[0] - tank.position[0], ene.position[1] - tank.position[1]
        angle3 = math.atan2(dy_ene, dx_ene)
        print(angle3)

        new_x_ene = 2 * math.cos(angle3)
        new_y_ene = 2 * math.sin(angle3)
        ene.position[0] -= new_x_ene
        ene.position[1] -= new_y_ene
        for b in bullets:
            if b.x > 1920 or b.x < 0 or b.y > 1080 or b.y < 0:
                bullets.remove(b)
            if b.x > ene.hitbox[0] and b.x < ene.hitbox[2] + ene.hitbox[0] and b.y > ene.hitbox[1] and b.y < ene.hitbox[1] + 100:
                ene.hit()
                bullets.remove(b)
            b.x += 10* math.cos(b.angle)
            b.y += 10* math.sin(b.angle)

        if ene.health < 0:
            enemies.remove(ene)
            enemies.append(Enemy(screen, [800, 500], f'{curr_dir}/image_game/mothership-0.92.png'))


    re_draw_all()
    

    
    # image_rotator.position[0] += joystick2.center[0] + joystick2.max_distance * math.cos(angle)
    # image_rotator.position[1] += joystick2.center[1] + joystick2.max_distance * math.sin(angle)



    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
