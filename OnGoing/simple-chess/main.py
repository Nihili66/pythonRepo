import sys
import pygame
from settings import *
from board import Board

class Game:
    def __init__(self):
        pygame.init()
        # setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for sprite in self.board.pieces:
                    if sprite.rect.colliderect(self.board.cursor.rect):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                sprite.dragging = True
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                sprite.dragging = False
                                for square in self.board.square_list:
                                    if square.rect.colliderect(self.board.cursor.rect):
                                        sprite.rect.center = square.rect.center
                        elif event.type == pygame.MOUSEMOTION:
                            if sprite.dragging:
                                sprite.rect.center = self.board.cursor.rect.center

            self.board.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
