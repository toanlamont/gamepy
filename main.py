import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

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

    def draw_man(self):
        if self.walk_count + 1 > 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1

            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1

        else:
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))


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


walk_right = [pygame.image.load(f'image_game/R{i}.png') for i in range(1, 10)]
walk_left = [pygame.image.load(f'image_game/L{i}.png') for i in range(1, 10)]
standing = pygame.image.load('image_game/standing.png')
bg = pygame.image.load('image_game/bg.jpg')
man = player(0, 0, 50, 50)
toan = player(50, 50, 50, 50)
bullets = []


def re_draw():
    win.blit(bg, (0, 0))
    man.draw_man()
    for b in bullets:
        b.draw_bullet()
    pygame.display.update()


run = True
clock = pygame.time.Clock()
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('im quit')
            run = False
        keys = pygame.key.get_pressed()

    for b in bullets:
        if b.x < 500 and b.x > 0:
            b.x += b.vel
        else:
            bullets.remove(b)

    if man.y < 450 - man.height:
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
    if keys[pygame.K_DOWN] and man.y < 450 - man.height:
        man.y += man.vel
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 6:
            bullets.append(bullet(x=(man.x + man.width / 2), y=(man.y + (man.height + 30) / 2), radius=6, color=color_dict['blue'], facing=facing))

    if man.is_jump:
        is_jump = False

    print(man.x, man.width)

    re_draw()

pygame.quit()