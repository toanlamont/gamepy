import pygame
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
CLOCK_RADIUS = 100
JOYSTICK_RADIUS = 50

# Colors
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clockwise Spinning Clock with Virtual Joystick")

# Clock variables
angle = 0  # Initial angle

# Initialize joystick
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No joystick found. Exiting...")
    pygame.quit()
    exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick input
    joystick_x = joystick.get_axis(0)
    joystick_y = joystick.get_axis(1)

    # Calculate the angle from joystick input
    angle = math.atan2(-joystick_y, joystick_x)

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the virtual joystick
    pygame.draw.circle(screen, WHITE, CENTER, JOYSTICK_RADIUS, 2)  # Outer circle
    joystick_pos = (CENTER[0] + joystick_x * JOYSTICK_RADIUS, CENTER[1] - joystick_y * JOYSTICK_RADIUS)
    pygame.draw.circle(screen, WHITE, joystick_pos, 10)  # Joystick knob

    # Draw the clock face
    pygame.draw.circle(screen, WHITE, CENTER, CLOCK_RADIUS)

    # Calculate the clock hand position
    hand_x = CENTER[0] + CLOCK_RADIUS * math.cos(angle)
    hand_y = CENTER[1] + CLOCK_RADIUS * math.sin(angle)

    # Draw the clock hand
    pygame.draw.line(screen, WHITE, CENTER, (hand_x, hand_y), 5)

    # Update the display
    pygame.display.flip()

pygame.quit()
