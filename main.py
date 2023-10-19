from typing import Any
import pygame
import random
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
display_info = pygame.display.Info()

# Get the screen resolution
screen_width = display_info.current_w
screen_height = display_info.current_h
win_size = (screen_width, screen_height)

# screen = pygame.display.set_mode((win_size[0], win_size[1]))
# screen = pygame.display.set_mode(win_size, pygame.FULLSCREEN)

# # pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.QUIT,
#                               pygame.FINGERUP, pygame.FINGERDOWN, pygame.KEYDOWN, pygame.KEYUP])
screen = pygame.display.set_mode(win_size)

pygame.display.set_caption("Joystick and Rotating Image")


class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, angle=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 20
        self.angle = angle
        self.image = pygame.image.load(image_path)
        self.image.set_colorkey((0,0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self) -> None:
        self.rect.centerx += 10 * math.cos(self.angle)
        self.rect.centery += 10 * math.sin(self.angle)


class EnemyBullet(bullet):
    def update(self) -> None:
        self.rect.centerx -= 10 * math.cos(self.angle)
        self.rect.centery -= 10 * math.sin(self.angle)


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


class Tank(pygame.sprite.Sprite):
    def __init__(self, screen, position, image_path):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.position = position
        self.angle = 0  # Initial angle
        self.health = 100
        self.image = pygame.image.load(image_path)
        self.org_img = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.hitbox = [self.rect.centerx - 50, self.rect.centery- 50, 100, 100]
        self.image = pygame.transform.rotate(self.org_img, -math.degrees(self.angle))
        self.image.set_colorkey((0,0,0,0))
        self.rect = self.image.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, color_dict['gray'], self.hitbox, 2)
        pygame.draw.rect(screen, color_dict['red'], (self.rect.centerx - 50, self.rect.centery - 50, 100, 10))
        pygame.draw.rect(screen, color_dict['navy'], (self.rect.centerx - 50, self.rect.centery - 50, self.health, 10))

    def hit(self):
        self.health -= 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, position, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.position = position
        self.image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
        self.org_img = self.image
        self.rect = self.image.get_rect()
        self.angle = 0  # Initial angle
        self.health = 10
        self.rect.center = position

    def update(self):
        # Create a rotated image
        self.hitbox = [self.rect.centerx - 50, self.rect.centery- 50, 100, 100]
        self.image = pygame.transform.rotate(self.org_img, -math.degrees(self.angle))
        self.image.set_colorkey((0,0,0,0))
        self.rect = self.image.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, color_dict['gray'], self.hitbox, 2)
        pygame.draw.rect(screen, color_dict['red'], (self.rect.centerx - 50, self.rect.centery - 50, 100, 10))
        pygame.draw.rect(screen, color_dict['navy'], (self.rect.centerx - 50, self.rect.centery - 50, self.health, 10))
    def hit(self):
        self.health -= 1

# Initialize Pygame

sprites = pygame.sprite.Group()


# Create a Joystick instance
joystick = Joystick(screen, (win_size[0] - 200, 800))
joystick2 = Joystick(screen, (200, 800))
curr_dir = (os.getcwd())


# Create an ImageRotator instance (provide the path to your image)
tank = Tank(screen, [500, 500], f'{curr_dir}/image_game/blue-tank-0.92.png')
enemy = Enemy(screen, [800, 500], f'{curr_dir}/image_game/mothership-0.92.png')
bullets = []
enemies = []
enemies_bullets = []
running = True
clock = pygame.time.Clock()
sprites.add(tank)


def re_draw_all():
    joystick.draw()
    joystick2.draw()
    sprites.update()
    sprites.draw(screen)

    if tank.rect.centerx < 100:
        for sprite in sprites:
            sprite.rect.move_ip(30, 0)

    elif tank.rect.centerx > win_size[0] - 100:
        for sprite in sprites:
            sprite.rect.move_ip(-30, 0)

    if tank.rect.centery < 100:
        for sprite in sprites:
            sprite.rect.move_ip(0, 30)

    elif tank.rect.centery > win_size[1] - 100:
        for sprite in sprites:
            sprite.rect.move_ip(0, -30)
    for ene in enemies:
        sprites.add(ene)


clock_count = 0
while running:
    clock.tick(27)
    clock_count += 1
    if clock_count > 60:
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
        tank.rect.centerx += new_x
        tank.rect.centery += new_y

    if joystick.moving and clock_count % 10 == 0:
        bu = (bullet(x=tank.rect.centerx + 100 * math.cos(tank.angle), y=tank.rect.centery + 100 * math.sin(tank.angle), angle=tank.angle, image_path=f'{curr_dir}/image_game/blue-bullet.png'))
        bullets.append(bu)
        sprites.add(bu)


    if len(enemies) == 0:
        for i in range(2):
            if tank.rect.centerx - 300 > 0 and tank.rect.centerx + 300 < win_size[0]:
                random_x = random.choice((random.randrange(0, tank.rect.centerx - 300), random.randrange(tank.rect.centerx + 300, win_size[0])))
            elif tank.rect.centerx - 300 < 0:
                random_x = random.randrange(random.randrange(tank.rect.centerx + 300, win_size[0]))
            elif tank.rect.centerx + 300 > win_size[0]:
                random_x = random.randrange(0, random.randrange(tank.rect.centerx - 300))

            if tank.rect.centery - 300 > 0 and tank.rect.centery + 300 < win_size[1]:
                random_y = random.choice((random.randrange(0, tank.rect.centery - 300), random.randrange(tank.rect.centery + 300, win_size[1])))
            elif tank.rect.centery - 300 < 0:
                random_y = random.randrange(random.randrange(tank.rect.centery + 300, win_size[1]))
            elif tank.rect.centery + 300 > win_size[1]:
                random_y = random.randrange(0, random.randrange(tank.rect.centery - 300))


            enemies.append(Enemy(screen, [random_x, random_y], f'{curr_dir}/image_game/mothership-0.92.png'))

    for ene in enemies:
        
        dx_ene, dy_ene = ene.rect.centerx - tank.rect.centerx, ene.rect.centery - tank.rect.centery
        angle3 = math.atan2(dy_ene, dx_ene)
        ene.angle = angle3

        new_x_ene = 2 * math.cos(angle3)
        new_y_ene = 2 * math.sin(angle3)
        ene.rect.centerx -= new_x_ene
        ene.rect.centery -= new_y_ene
        for b in bullets:
            try:
                if b.rect.centerx > win_size[0] or b.rect.centerx < 0 or b.rect.centery > win_size[1] or b.rect.centery < 0:
                    bullets.remove(b)
                    sprites.remove(b)
                if b.rect.centerx > ene.hitbox[0] and b.rect.centerx < ene.hitbox[2] + ene.hitbox[0] and b.rect.centery > ene.hitbox[1] and b.rect.centery < ene.hitbox[1] + 100 and len(enemies) != 0:
                    ene.hit()
                    bullets.remove(b)
                    sprites.remove(b)
            except:
                continue


        if ene.health < 0:
            enemies.remove(ene)
            sprites.remove(ene)

        #     enemies.append(Enemy(screen, [800, 500], f'{curr_dir}/image_game/mothership-0.92.png'))
        if clock_count // 60  == 1:
            ene_bu = (EnemyBullet(x=ene.rect.centerx + 100 * math.cos(ene.angle), y=ene.rect.centery + 100 * math.sin(ene.angle), angle=ene.angle, image_path=f'{curr_dir}/image_game/trigonship.png'))
            enemies_bullets.append(ene_bu)
            print('append', clock_count // 60)
            sprites.add(ene_bu)
        for ene_bu in enemies_bullets:
            if ene_bu.rect.centerx > win_size[0] or ene_bu.rect.centerx < 0 or ene_bu.rect.centery > win_size[1] or ene_bu.rect.centery < 0:
                enemies_bullets.remove(ene_bu)
            if ene_bu.rect.centerx > tank.hitbox[0] and ene_bu.rect.centerx < tank.hitbox[2] + tank.hitbox[0] and ene_bu.rect.centery > tank.hitbox[1] and ene_bu.rect.centery < tank.hitbox[1] + 100:
                # ene.hit()
                enemies_bullets.remove(ene_bu)
                sprites.remove(ene_bu)

    # print(clock_count // 27)
    re_draw_all()
    

    
    # image_rotator.position[0] += joystick2.center[0] + joystick2.max_distance * math.cos(angle)
    # image_rotator.position[1] += joystick2.center[1] + joystick2.max_distance * math.sin(angle)



    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
