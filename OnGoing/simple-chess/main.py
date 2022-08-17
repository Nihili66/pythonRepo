import sys
import pygame
import pygame_gui
from gui import Welcomegui
from settings import *
from board import Board
from movement import move_piece

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chess Game')
        # general setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.background = pygame.Surface((WIDTH, HEIGTH))
        self.background.fill(pygame.Color('#000000'))
        self.clock = pygame.time.Clock()
        # gui setup
        self.gui = Welcomegui()
        # board init
        self.board = None

    def run(self):
        while True:
            time_delta = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.board:
                    move_piece(self.board, event)
                self.gui.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gui.start_button:
                        self.gui.manager.clear_and_reset()
                        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

            if self.board:
                self.board.run()
            self.gui.manager.update(time_delta)
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
            self.gui.manager.draw_ui(self.screen)


if __name__ == '__main__':
    game = Game()
    game.run()
