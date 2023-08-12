import sys
import pygame
from settings import *
from gmanager import GManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Checkers Game')
        # general setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.background = pygame.Surface((WIDTH, HEIGTH))
        self.background.fill(pygame.Color('#000000'))
        self.clock = pygame.time.Clock()
        self.gm = GManager()
        self.gm.game_init("human", "human")

    def run(self):
        while True:
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # game events
                self.gm.game_play(event)

            self.gm.update()
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
