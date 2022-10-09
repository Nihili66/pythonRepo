import pygame
import sys
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Betting Game')
        # general setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(pygame.Color('#000000'))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(FPS)
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))


if __name__ == '__main__':
    game = Game()
    game.run()
