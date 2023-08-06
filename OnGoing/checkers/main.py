import sys
import pygame
from settings import *
from board import Board


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Checkers Game')
        # general setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.background = pygame.Surface((WIDTH, HEIGTH))
        self.background.fill(pygame.Color('#000000'))
        self.clock = pygame.time.Clock()
        self.board = Board()

    def run(self):
        while True:
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.board.run()
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
