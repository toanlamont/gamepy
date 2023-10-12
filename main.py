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
run = True
is_jump = False
jump_count = 5
x = 0
y = 0
w = 50
h = 50
vel = 5

walk_count = 0

walk_right = [pygame.image.load(f'image_game/R{i}.png') for i in range(1, 10)]
walk_left = [pygame.image.load(f'image_game/L{i}.png') for i in range(1, 10)]
standing = pygame.image.load('image_game/standing.png')
bg = pygame.image.load('image_game/bg.jpg')


left = False
right = False


def re_draw():
    global walk_count
    win.blit(bg, (0, 0))
    if walk_count + 1 > 27:
        walk_count = 0
    if left:
        win.blit(walk_left[walk_count//3], (x, y))
        walk_count += 1

    elif right:
        win.blit(walk_right[walk_count//3], (x, y))
        walk_count += 1

    else:
        win.blit(standing, (x, y))

     
    # pygame.draw.rect(win, color_dict['indigo'], (x, y, w, h))
    pygame.display.update()



while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('im quit')
            run = False
        keys = pygame.key.get_pressed()

    if y <450 - h:
        y += 1
    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
        left = True
        right = False

    elif keys[pygame.K_RIGHT] and x < 450:
        x += vel
        left = False
        right = True

    else:
        right = False
        left = False
        walk_count = 0

    if keys[pygame.K_UP] and y > 0:
        y -= vel
    if keys[pygame.K_DOWN] and y <450 - h:
        y += vel
    if keys[pygame.K_SPACE]:
        is_jump = True
        left = False
        right = False

    if is_jump:
        y -= jump_count
        is_jump = False

    re_draw()

    
pygame.quit()