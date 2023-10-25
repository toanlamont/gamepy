import pygame
import random
import sys
import math
import os


color_dict = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (139, 69, 19),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "lime": (0, 255, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "violet": (238, 130, 238),
    "indigo": (75, 0, 130),
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
    def __init__(self, x, y, image_path, angle=None, speed=5) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 20
        self.angle = angle
        self.image = pygame.image.load(image_path)
        self.image.set_colorkey((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self) -> None:
        self.rect.centerx += self.speed * math.cos(self.angle)
        self.rect.centery += self.speed * math.sin(self.angle)


class Object(pygame.sprite.Sprite):
    def __init__(self, position, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (100, 100)
        )
        self.org_img = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.cooldown_bullet = 0
        self.hitbox = [
            self.rect.centerx - 75,
            self.rect.centery - 75,
            150,
            150,
        ]
        self.image.set_colorkey((0, 0, 0, 0))

    def update(self):
        pass


class EnemyBullet(bullet):
    def update(self) -> None:
        self.rect.centerx -= 2 * math.cos(self.angle)
        self.rect.centery -= 2 * math.sin(self.angle)


class Joystick:
    def __init__(
        self,
        screen,
        position,
        background_radius=150,
        handle_radius=100,
        max_distance=100,
        color=(255, 255, 255),
    ):
        self.screen = screen
        self.position = position
        self.background_radius = background_radius
        self.handle_radius = handle_radius
        self.max_distance = max_distance
        self.color = color
        self.center = self.position
        self.moving = False
        self.angle = None
        self.motion = False

    def draw(self):
        # Draw the joystick background
        pygame.draw.circle(
            self.screen, (255, 0, 0), self.center, self.background_radius
        )

        # Draw the movable joystick handle
        pygame.draw.circle(
            self.screen, (128, 128, 128, 50), self.position, self.handle_radius
        )

    def update(self, event):
        if event.type == pygame.FINGERDOWN:
            mouse_x, mouse_y = (
                event.dict["x"] * win_size[0],
                event.dict["y"] * win_size[1],
            )
            distance = math.hypot(
                mouse_x - self.position[0], mouse_y - self.position[1]
            )
            if distance <= self.background_radius:
                self.moving = True
        elif event.type == pygame.FINGERMOTION and self.moving:
            self.motion = True
            mouse_x, mouse_y = (
                event.dict["x"] * win_size[0],
                event.dict["y"] * win_size[1],
            )

            dx = mouse_x - self.center[0]
            dy = mouse_y - self.center[1]
            distance = math.hypot(dx, dy)
            if distance > self.max_distance:
                angle = math.atan2(dy, dx)
                self.angle = angle
                new_x = self.center[0] + self.max_distance * math.cos(
                    angle
                )
                new_y = self.center[1] + self.max_distance * math.sin(
                    angle
                )
            else:
                new_x, new_y = mouse_x, mouse_y
            self.position = (new_x, new_y)

        elif event.type == pygame.FINGERUP:
            self.moving = False
            self.motion = False
            self.position = self.center

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            distance = math.hypot(
                mouse_x - self.position[0], mouse_y - self.position[1]
            )
            if distance <= self.background_radius:
                self.moving = True
        elif event.type == pygame.MOUSEMOTION and self.moving:
            self.motion = True
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
            self.motion = False
            self.position = self.center


class Tank(pygame.sprite.Sprite):
    def __init__(self, screen, position, image_path, cooldown=60, speed=10):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.position = position
        self.angle = 0  # Initial angle
        self.health = 10
        self.image = pygame.image.load(image_path)
        self.org_img = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.die = 0
        self.cooldown = cooldown
        self.cooldown_bullet = 0
        self.hitbox = [
            self.rect.centerx - 50,
            self.rect.centery - 50,
            100,
            100,
        ]
        self.speed = speed

    def update(self):
        self.hitbox = [
            self.rect.centerx - 50,
            self.rect.centery - 50,
            100,
            100,
        ]
        self.image = pygame.transform.rotate(
            self.org_img, -math.degrees(self.angle)
        )
        self.image.set_colorkey((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=self.rect.center)
        # pygame.draw.rect(screen, color_dict['gray'], self.hitbox, 2)
        pygame.draw.rect(
            screen,
            color_dict["red"],
            (self.rect.centerx - 50, self.rect.centery - 50, 100, 10),
        )
        pygame.draw.rect(
            screen,
            color_dict["navy"],
            (
                self.rect.centerx - 50,
                self.rect.centery - 50,
                10 * self.health,
                10,
            ),
        )

    def hit(self):
        self.health -= 1

    def hit_object(self, object_game):
        if (
            abs(self.rect.centerx - object_game.rect.centerx) < 100
            and abs(self.rect.centery - object_game.rect.centery) < 100
        ):
            return True

        else:
            return False


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        screen,
        position,
        image_path,
        speed=1,
        damage=0.5,
        bullet_speed=1,
        cooldown=200,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.position = position
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (100, 100)
        )
        self.org_img = self.image
        self.rect = self.image.get_rect()
        self.angle = 0  # Initial angle
        self.health = 10
        self.rect.center = position
        self.speed = speed
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.cooldown = cooldown
        self.cooldown_bullet = 0

    def update(self):
        # Create a rotated image
        self.hitbox = [
            self.rect.centerx - 50,
            self.rect.centery - 50,
            100,
            100,
        ]
        self.image = pygame.transform.rotate(
            self.org_img, -math.degrees(self.angle)
        )
        self.image.set_colorkey((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=self.rect.center)
        # pygame.draw.rect(screen, color_dict['gray'], self.hitbox, 2)
        pygame.draw.rect(
            screen,
            color_dict["red"],
            (self.rect.centerx - 50, self.rect.centery - 50, 100, 10),
        )
        pygame.draw.rect(
            screen,
            color_dict["navy"],
            (
                self.rect.centerx - 50,
                self.rect.centery - 50,
                10 * self.health,
                10,
            ),
        )

    def hit(self):
        self.health -= 1


class Text:
    def __init__(self, x, y, color, font_size) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.SysFont("comicsans", self.font_size, True)
        self.border_font = pygame.font.SysFont(
            "comicsans", self.font_size + 4, True
        )
        self.hightlight = False

    def draw(self, text, hightlight=False):
        text_surface = self.font.render(str(text), True, self.color)
        text_border = self.border_font.render(str(text), True, "grey")
        if hightlight:
            screen.blit(text_border, (self.x - 2, self.y - 2))
        screen.blit(text_surface, (self.x, self.y))


# Initialize Pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Menu", True, (0, 0, 0))
        self.textpos = self.text.get_rect(
            centerx=self.background.get_width() / 2,
            centery=self.background.get_height() / 2,
        )
        self.continue_game = Text(500, 500, "red", 50)

        self.high_score = Text(100, 100, "black", 50)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
                    elif event.key == pygame.K_SPACE:
                        return "game"
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    for t in [self.high_score, self.continue_game]:
                        if (t.x < mouse_x < t.x + 200) and (t.y < mouse_y < t.y + 50):
                            t.hightlight = True
                        else:
                            t.hightlight = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for t in [self.high_score, self.continue_game]:
                        if (t.x < mouse_x < t.x + 200) and (t.y < mouse_y < t.y + 50):
                            if t == self.continue_game:
                                return "game"

            self.screen.blit(self.background, (0, 0))
            self.high_score.draw("High score", self.high_score.hightlight)
            self.continue_game.draw(
                "Continue game", self.continue_game.hightlight
            )

            pygame.display.flip()


class GamePlay:
    def __init__(self) -> None:
        self.running = True
        self.joystick = Joystick(screen, (win_size[0] - 300, 700))
        self.joystick2 = Joystick(screen, (300, 700))
        self.curr_dir = os.getcwd()
        self.sprites = pygame.sprite.Group()

        # Create an ImageRotator instance (provide the path to your image)
        self.tank = Tank(
            screen,
            [500, 500],
            f"{self.curr_dir}/image_game/blue-tank-0.92.png",
        )
        self.enemy = Enemy(
            screen,
            [800, 500],
            f"{self.curr_dir}/image_game/mothership-0.92.png",
        )
        self.heal = Object(
            (100, 100), image_path=f"{self.curr_dir}/image_game/health.png"
        )
        self.cross = Object(
            (200, 100), image_path=f"{self.curr_dir}/image_game/cross.png"
        )
        self.bullets = []
        self.enemies = []
        self.enemies_bullets = []
        self.level = 0
        self.clock = pygame.time.Clock()
        self.sprites.add(self.tank)
        # self.sprites.add(heal, cross)

        self.score = 0
        self.score_text = Text(100, 100, color_dict["brown"], 30)
        self.die = 0
        self.clock_count = 0
        self.cooldown_bullet = 0
        self.cooldown_health = 100
        self.cooldown_shot = 100
        self.healths = []
        self.shots = []

    def re_draw_all(self):
        if not self.die:
            self.joystick.draw()
            self.joystick2.draw()
            self.sprites.update()
            self.sprites.draw(screen)
            self.score_text.draw(f"Scores: {self.score}")

            if self.tank.rect.centerx < 100:
                for sprite in self.sprites:
                    for i in range(30):
                        sprite.rect.move_ip(1, 0)

            elif self.tank.rect.centerx > win_size[0] - 100:
                for sprite in self.sprites:
                    for i in range(30):
                        sprite.rect.move_ip(-1, 0)

            if self.tank.rect.centery < 100:
                for sprite in self.sprites:
                    for i in range(30):
                        sprite.rect.move_ip(0, 1)

            elif self.tank.rect.centery > win_size[1] - 100:
                for sprite in self.sprites:
                    for i in range(30):
                        sprite.rect.move_ip(0, -1)
            for ene in self.enemies:
                self.sprites.add(ene)

        else:
            screen.blit()

    def run(self):
        print("running")
        while self.running:
            self.clock.tick(60)

            if self.tank.cooldown_bullet > 0:
                self.tank.cooldown_bullet -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                self.joystick.update(event)
                self.joystick2.update(event)

            screen.fill((255, 255, 255))  # Clear the screen

            if self.tank.health <= 0:
                self.tank.die = 1
                self.sprites.remove(self.tank)
                print("die")
                return "menu"

            if self.cooldown_health > 0:
                self.cooldown_health -= 1

            if self.cooldown_health == 0 and len(self.healths) == 0:
                health = Object(
                    position=(
                        random.randrange(1, win_size[0]),
                        random.randrange(1, win_size[1]),
                    ),
                    image_path=f"{self.curr_dir}/image_game/health.png",
                )
                self.sprites.add(health)
                self.healths.append(health)
                self.cooldown_health = 100

            for health in self.healths:
                if self.tank.hit_object(health):
                    self.tank.health += 1
                    self.healths.remove(health)
                    self.sprites.remove(health)

            # Update the angle of the rotating image based on self.joystick position
            dx, dy = (
                self.joystick.position[0] - self.joystick.center[0],
                self.joystick.position[1] - self.joystick.center[1],
            )
            angle = math.atan2(dy, dx)
            if self.joystick.motion:
                self.tank.angle = angle

            dx2, dy2 = (
                self.joystick2.position[0] - self.joystick2.center[0],
                self.joystick2.position[1] - self.joystick2.center[1],
            )
            angle2 = math.atan2(dy2, dx2)

            new_x = self.tank.speed * math.cos(angle2)
            new_y = self.tank.speed * math.sin(angle2)
            if int(new_x) == 40:
                new_x = 0
            if self.joystick2.motion:
                self.tank.rect.centerx += new_x
                self.tank.rect.centery += new_y

            if self.joystick.motion and self.tank.cooldown_bullet == 0:
                bu = bullet(
                    x=self.tank.rect.centerx + 100 * math.cos(self.tank.angle),
                    y=self.tank.rect.centery + 100 * math.sin(self.tank.angle),
                    angle=self.tank.angle,
                    image_path=f"{self.curr_dir}/image_game/blue-bullet.png",
                )
                self.bullets.append(bu)
                self.sprites.add(bu)
                self.tank.cooldown_bullet = self.tank.cooldown

            if len(self.enemies) == 0:
                for i in range(2):
                    if (
                        self.tank.rect.centerx - 300 > 0
                        and self.tank.rect.centerx + 300 < win_size[0]
                    ):
                        random_x = random.choice(
                            (
                                random.randrange(
                                    0, self.tank.rect.centerx - 300
                                ),
                                random.randrange(
                                    self.tank.rect.centerx + 300, win_size[0]
                                ),
                            )
                        )
                    elif self.tank.rect.centerx - 300 < 0:
                        random_x = random.randrange(
                            random.randrange(
                                self.tank.rect.centerx + 300, win_size[0]
                            )
                        )
                    elif self.tank.rect.centerx + 300 > win_size[0]:
                        random_x = random.randrange(
                            0, random.randrange(self.tank.rect.centerx - 300)
                        )

                    if (
                        self.tank.rect.centery - 300 > 0
                        and self.tank.rect.centery + 300 < win_size[1]
                    ):
                        random_y = random.choice(
                            (
                                random.randrange(
                                    0, self.tank.rect.centery - 300
                                ),
                                random.randrange(
                                    self.tank.rect.centery + 300, win_size[1]
                                ),
                            )
                        )
                    elif self.tank.rect.centery - 300 < 0:
                        random_y = random.randrange(
                            random.randrange(
                                self.tank.rect.centery + 300, win_size[1]
                            )
                        )
                    elif self.tank.rect.centery + 300 > win_size[1]:
                        random_y = random.randrange(
                            0, random.randrange(self.tank.rect.centery - 300)
                        )

                    self.enemies.append(
                        Enemy(
                            screen,
                            [random_x, random_y],
                            f"{self.curr_dir}/image_game/mothership-0.92.png",
                        )
                    )

            for ene in self.enemies:
                if ene.cooldown_bullet > 0:
                    ene.cooldown_bullet -= 1

                if self.tank.hit_object(ene):
                    self.tank.health -= 5
                    self.sprites.remove(ene)
                    self.enemies.remove(ene)

                dx_ene, dy_ene = (
                    ene.rect.centerx - self.tank.rect.centerx,
                    ene.rect.centery - self.tank.rect.centery,
                )
                angle3 = math.atan2(dy_ene, dx_ene)
                ene.angle = angle3

                new_x_ene = ene.speed * math.cos(angle3)
                new_y_ene = ene.speed * math.sin(angle3)
                print(new_x_ene, new_y_ene)
                ene.rect.centerx -= new_x_ene
                ene.rect.centery -= new_y_ene
                for b in self.bullets:
                    try:
                        if (
                            b.rect.centerx > win_size[0]
                            or b.rect.centerx < 0
                            or b.rect.centery > win_size[1]
                            or b.rect.centery < 0
                        ):
                            self.bullets.remove(b)
                            self.sprites.remove(b)
                        if (
                            b.rect.centerx > ene.hitbox[0]
                            and b.rect.centerx < ene.hitbox[2] + ene.hitbox[0]
                            and b.rect.centery > ene.hitbox[1]
                            and b.rect.centery < ene.hitbox[1] + 100
                            and len(self.enemies) != 0
                        ):
                            ene.hit()
                            self.bullets.remove(b)
                            self.sprites.remove(b)
                    except Exception:
                        continue

                if ene.health < 0:
                    self.enemies.remove(ene)
                    self.sprites.remove(ene)
                    self.score += 1

                #     enemies.append(Enemy(screen, [800, 500], f'{self.curr_dir}/image_game/mothership-0.92.png'))
                if ene.cooldown_bullet == 0:
                    ene_bu = EnemyBullet(
                        x=ene.rect.centerx + 100 * math.cos(ene.angle),
                        y=ene.rect.centery + 100 * math.sin(ene.angle),
                        angle=ene.angle,
                        image_path=f"{self.curr_dir}/image_game/trigonship.png",
                    )
                    self.enemies_bullets.append(ene_bu)
                    self.sprites.add(ene_bu)
                    ene.cooldown_bullet = ene.cooldown
                for ene_bu in self.enemies_bullets:
                    if (
                        ene_bu.rect.centerx > win_size[0]
                        or ene_bu.rect.centerx < 0
                        or ene_bu.rect.centery > win_size[1]
                        or ene_bu.rect.centery < 0
                    ):
                        self.enemies_bullets.remove(ene_bu)
                        self.sprites.remove(ene_bu)
                    if (
                        ene_bu.rect.centerx > self.tank.hitbox[0]
                        and ene_bu.rect.centerx
                        < self.tank.hitbox[2] + self.tank.hitbox[0]
                        and ene_bu.rect.centery > self.tank.hitbox[1]
                        and ene_bu.rect.centery < self.tank.hitbox[1] + 100
                    ):
                        self.tank.hit()
                        self.enemies_bullets.remove(ene_bu)
                        self.sprites.remove(ene_bu)

                    for bu in self.bullets:
                        try:
                            if (
                                abs(bu.rect.centerx - ene_bu.rect.centerx) < 50
                                and abs(bu.rect.centery - ene_bu.rect.centery)
                                < 50
                            ):
                                self.enemies_bullets.remove(ene_bu)
                                self.sprites.remove(ene_bu)
                        except Exception:
                            pass

            self.re_draw_all()

            pygame.display.flip()  # Update the display


class App:
    def __init__(self) -> None:
        pass

    def run(self):
        menuplay = Menu(screen=screen)
        gameplay = GamePlay()

        pl = menuplay.run()
        while pl:
            if pl == "game":
                gameplay.tank.health = 10
                gameplay.sprites.add(gameplay.tank)
                gameplay.joystick.moving = False
                gameplay.joystick2.moving = False
                gameplay.joystick.position = gameplay.joystick.center
                gameplay.joystick2.position = gameplay.joystick2.center

                print(gameplay.__dict__)
                pl = gameplay.run()
            if pl == "menu":
                pl = menuplay.run()
            if pl == "quit":
                break


a = App()
a.run()

pygame.quit()
sys.exit()
