import pygame
import sys

def main():
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Play Sound on Event")

    # Load sound file
    break_sound = pygame.mixer.Sound('image_game/break.mp3')
    shot_sound = pygame.mixer.Sound('image_game/shot.mp3')


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Play sound on space key press
                    break_sound.play()

                elif event.key == pygame.K_UP:
                    shot_sound.play()


            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        # Draw something here if needed
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
