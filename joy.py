import pygame
pygame.init()

# Create Pygame window
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Virtual Joystick")

# Define joystick graphics
joystick_radius = 50
joystick_color = (0, 0, 255)
joystick_position = (screen_width // 2, screen_height // 2)

base_width = 100
base_height = 100
base_color = (200, 200, 200)
base_position = (screen_width // 2 - base_width // 2, screen_height // 2 - base_height // 2)

# Define the Player class
class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

# Initialize the player
player = Player(screen_width // 2, screen_height // 2, 5)

# Main Game Loop
running = True
joystick_grabbed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(base_position[0], base_position[1], base_width, base_height).collidepoint(event.pos):
                joystick_grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            joystick_grabbed = False
            joystick_position = (screen_width // 2, screen_height // 2)  # Reset to center

    if joystick_grabbed:
        joystick_position = pygame.mouse.get_pos()
        dx = (joystick_position[0] - base_position[0]) / joystick_radius
        dy = (joystick_position[1] - base_position[1]) / joystick_radius
        player.update(dx / 5, dy/ 5)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the base
    pygame.draw.rect(screen, base_color, (base_position[0], base_position[1], base_width, base_height))

    # Draw the joystick
    pygame.draw.circle(screen, joystick_color, joystick_position, joystick_radius)

    # Draw the player object
    pygame.draw.rect(screen, (255, 0, 0), (player.x, player.y, 20, 20))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
