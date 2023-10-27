import pygame
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Multi-line Text")

# Create a font object
font = pygame.font.Font(None, 36)

# Text with newline character
text = "This is the first line.\nThis is the second line."

# Split the text into lines
lines = text.split('\n')

# Render each line separately
text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Blit each line onto the screen with appropriate vertical spacing
    for i, text_surface in enumerate(text_surfaces):
        screen.blit(text_surface, (50, 50 + i * 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
