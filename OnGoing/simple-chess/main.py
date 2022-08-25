import sys
import pygame
import pygame_gui
from gui import Welcomegui
from settings import *
from sprites import Player
from board import Board


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
        # players init
        self.whiteP = None
        self.blackP = None
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
                    if self.whiteP.turn:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.whiteP.movement.clicking(event)
                        if self.whiteP.movement.piece:
                            if event.type == pygame.MOUSEBUTTONUP:
                                if event.button == 1:
                                    self.whiteP.movement.putting(event)
                            if event.type == pygame.MOUSEMOTION:
                                self.whiteP.movement.dragging()
                    if self.blackP.turn:
                        self.blackP.movement.pick_move()
                        if self.blackP.movement.piece:
                            self.blackP.movement.invoke_move()
                self.gui.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gui.start_button:
                        self.gui.manager.clear_and_reset()
                        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
                        self.whiteP = Player("white", "human", self.board, self.board.players)
                        self.blackP = Player("black", "AI", self.board, self.board.players)

            if self.board:
                self.board.run()
            self.gui.manager.update(time_delta)
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
            self.gui.manager.draw_ui(self.screen)


if __name__ == '__main__':
    game = Game()
    game.run()
