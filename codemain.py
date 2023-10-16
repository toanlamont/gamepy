import pygame
import math
import os

pygame.init()

# win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
win = pygame.display.set_mode((900, 500))


pygame.display.set_caption("first game")

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
curr_dir = (os.getcwd())

transparent_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  # Use SRCALPHA for transparency

# Brown color with an alpha value of 128 (semi-transparent)
brown_color = (139, 69, 19, 100)
violet = (238, 130, 238, 100)


# Position of the transparent object




class player():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.walk_right = [pygame.image.load(f'{curr_dir}/image_game/R{i}.png') for i in range(1, 10)]
        self.walk_left = [pygame.image.load(f'{curr_dir}/image_game/L{i}.png') for i in range(1, 10)]
        self.standing = pygame.image.load(f'{curr_dir}/image_game/standing.png')
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def draw_man(self):
        if self.walk_count + 1 > 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                win.blit(self.walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1

            elif self.right:
                win.blit(self.walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1

        else:
            if self.left:
                win.blit(self.walk_left[0], (self.x, self.y))
            else:
                win.blit(self.walk_right[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 5, 28, 60)
        pygame.draw.rect(win, color_dict['navy'], self.hitbox, 2)


class bullet():
    def __init__(self, x, y, radius, color, facing) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.color = color
        self.vel = 20 * facing

    def draw_bullet(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class button():
    def __init__(self, x, y, radius, color, clicked_color) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = brown_color
        self.clicked_color = violet
        self.display_color = color
        self.is_clicking = False

    def draw_button(self):
        if self.is_clicking:
            pygame.draw.circle(transparent_surface, brown_color, (50, 50), 50)
            win.blit(transparent_surface, (self.x - 50, self.y - 50))
        else:
            pygame.draw.circle(transparent_surface, violet, (50, 50), 50)
            win.blit(transparent_surface, (self.x - 50, self.y  - 50))
            

    def is_click(self, clicked_point):
        x, y = clicked_point
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance <= self.radius


class enemy():
    def __init__(self, x, y, width, height, end) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.end = end
        self.vel = 3
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.walk_right = [pygame.image.load(f'{curr_dir}/image_game/R{i}E.png') for i in range(1, 12)]
        self.walk_left = [pygame.image.load(f'{curr_dir}/image_game/L{i}E.png') for i in range(1, 12)]
        self.health = 10
        self.die = False

    def draw_enemy(self):
        if self.health > 0:
            if self.walk_count > 27:
                self.walk_count = 0
            if self.vel > 0:
                if self.x > 450:
                    self.vel *= -1
                else:
                    win.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                    self.x += self.vel
            else:
                if self.x < 50:
                    self.vel *= -1
                else:
                    win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                    self.x += self.vel
            self.walk_count += 1
            self.hitbox = (self.x + 15, self.y + 5, 30, 55)
            pygame.draw.rect(win, color_dict['red'], (self.x, self.y, 50, 10))
            pygame.draw.rect(win, color_dict['navy'], (self.x, self.y, 5 * self.health, 10))

        else:
            self.hitbox = [0,0,0,0]


    def hit(self):
        print('hit')
        self.health -= 1
        






bg = pygame.image.load(f'{curr_dir}/image_game/bg.jpg')
man = player(0, 0, 50, 50)
toan = player(50, 50, 50, 50)
fire_button = button(x=400, y=400, radius=50, color=(255,0,0, 100), clicked_color=color_dict['gold'])
gob = enemy(200, 420, 30, 50, 450)
bullets = []


def re_draw():
    win.blit(bg, (0, 0))
    man.draw_man()
    fire_button.draw_button()
    gob.draw_enemy()
    for b in bullets:
        b.draw_bullet()
    text = font.render("score: " + str(score), True, color_dict['brown'])
    win.blit(text, (300, 0))
    pygame.display.update()


run = True
score = 0
font = pygame.font.SysFont("comicsans", 30, True)
clock = pygame.time.Clock()
button_clicked = False
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('im quit')
            run = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.FINGERDOWN:
            print(event.dict)
        if event.type == pygame.FINGERUP:
            fire_button.is_clicking = False
    for b in bullets:
        if b.x < 500 and b.x > 0:
            b.x += b.vel
        else:
            bullets.remove(b)
        if b.x > gob.x and b.x < gob.x + gob.hitbox[2] and b.y > gob.y and b.y < gob.y + gob.hitbox[3]:
            gob.hit()
            score += 1
            bullets.remove(b)

    if man.y < 460 - man.height:
        man.y += 1
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 450:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True
        walk_count = 0

    if keys[pygame.K_UP] and man.y > 0:
        man.y -= man.vel
    if keys[pygame.K_DOWN] and man.y < 460 - man.height:
        man.y += man.vel
    if keys[pygame.K_SPACE] or fire_button.is_clicking:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 6:
            bullets.append(bullet(x=(man.x + man.width / 2), y=(man.y + (man.height + 30) / 2), radius=6, color=color_dict['blue'], facing=facing))

    if man.is_jump:
        is_jump = False

    re_draw()

pygame.quit()