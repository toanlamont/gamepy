import pygame
import random

pygame.init()
display_info = pygame.display.Info()

# Get the screen resolution
screen_width = display_info.current_w
screen_height = display_info.current_h

# define screen size
SCREEN_WIDTH = screen_width
SCREEN_HEIGHT = screen_height
print(screen_width, screen_height)

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Groups")

# frame rate
clock = pygame.time.Clock()
FPS = 60

# colours
colours = [
    "crimson",
    "chartreuse",
    "coral",
    "darkorange",
    "forestgreen",
    "lime",
    "navy",
]
ar = 1


# create class for squares
class Square(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # self.rect.move_ip(0, 5 * ar)
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.dx = 1
        self.rect.center = (x, y)

    def update(self):
        self.rect.move(self.dx, 0)



# create sprite group for squares
squares = pygame.sprite.Group()
player = Player(100, 100)
# create square and add to squares group
square = Square("crimson", 500, 300)
squares.add(square)
squares.add(player)

# game loop
run = True
while run:
    clock.tick(FPS)

    # update background
    screen.fill("cyan")

    # update sprite group
    squares.update()

    # draw sprite group
    squares.draw(screen)

    if len(squares) == 30:
        ar *= -1

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse coordinates
            pos = pygame.mouse.get_pos()
            # create square
            square = Square(random.choice(colours), pos[0], pos[1])
            squares.add(square)
        # quit program
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            run = False
        if keys[pygame.K_LEFT]:
            print('left')
            player.rect.centerx -= 10

        if keys[pygame.K_RIGHT]:
            print('left')
            player.rect.centerx += 10

        if keys[pygame.K_SPACE]:
            print('space')

    if player.rect.centerx < 100:
        for s in squares:
            s.rect.move_ip(1, 0)

    if player.rect.centerx > SCREEN_WIDTH - 100:
        for s in squares:
            s.rect.move_ip(-1, 0)


    # update display
    pygame.display.flip()

pygame.quit()
