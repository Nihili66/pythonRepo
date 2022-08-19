import sys
import pygame
import pygame_gui
from gui import Welcomegui
from settings import *
from board import Board
from movement import MovementLogic

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
        # movement logic init
        self.movement = None

    def run(self):
        while True:
            time_delta = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.board:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.movement.clicking(event)
                    if self.movement.piece:
                        if event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                self.movement.putting(event)
                        if event.type == pygame.MOUSEMOTION:
                            self.movement.dragging()
                self.gui.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gui.start_button:
                        self.gui.manager.clear_and_reset()
                        self.board = Board("K6K/N6N/3q4/2q1q3/3P4/N7/7N/K6K")
                        self.movement = MovementLogic(self.board)

            if self.board:
                self.board.run()
            self.gui.manager.update(time_delta)
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
            self.gui.manager.draw_ui(self.screen)


if __name__ == '__main__':
    game = Game()
    game.run()
