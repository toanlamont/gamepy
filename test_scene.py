import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Menu", True, (0, 0, 0))
        self.textpos = self.text.get_rect(centerx=self.background.get_width()/2,
                                          centery=self.background.get_height()/2)

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

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.text, self.textpos)
            pygame.display.flip()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0, 0, 255))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Game", True, (255, 255, 255))
        self.textpos = self.text.get_rect(centerx=self.background.get_width()/2,
                                          centery=self.background.get_height()/2)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
                    elif event.key == pygame.K_SPACE:
                        return "menu"

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.text, self.textpos)
            pygame.display.flip()

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))

    def run(self):
        while True:
            menu = Menu(self.screen)
            status_menu = menu.run()
            if status_menu == "quit":
                pygame.quit()
                break

            game = Game(self.screen)
            status_game = game.run()
            if status_game == "quit":
                pygame.quit()
                break

if __name__ == "__main__":
    app = App()
    app.run()
