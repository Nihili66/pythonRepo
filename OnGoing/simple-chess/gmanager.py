import pygame
import pygame_gui
from settings import *
from sprites import Player
from board import Board

class GManager:
    def __init__(self):
        # players init
        self.whiteP = None
        self.blackP = None
        # board init
        self.board = None
        # gui init
        self.manager = pygame_gui.UIManager((WIDTH, HEIGTH))
        # welcome screen
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 2 - 60, HEIGTH / 2 - 25), (120, 50)),
                                                         text='Start Game',
                                                         manager=self.manager)

    def game_init(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.manager.clear_and_reset()
                self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", self)
                self.board.run()
                self.whiteP = Player("white", "human", self.board)
                self.board.players.append(self.whiteP)
                self.blackP = Player("black", "AI", self.board)
                self.board.players.append(self.blackP)
                timers_init(self)

    def game_play(self, event):
        if self.board:
            for player in self.board.players:
                if player.turn and player.type == "human":
                    player.movement.pick_move(event)
                    if player.movement.piece:
                        player.movement.play_move(event)
                elif player.turn and player.type == "AI":
                    player.movement.pick_move()
                    if player.movement.move:
                        player.movement.play_move()

    def game_over(self, winner):
        self.whiteP.kill()
        self.blackP.kill()
        self.board.players = []
        game_over_screen(self, winner)

    def update(self, time_delta, screen):
        if self.board:
            self.board.run()
        self.manager.update(time_delta)
        self.manager.draw_ui(screen)

def timers_init(self):
    # player clock timers (wip)
    white_timer = 200
    if self.whiteP.turn:
        white_timer -= 1
    black_timer = 200
    if self.blackP.turn:
        black_timer -= 1
    # player clock timers ui
    self.white_clock = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((560, 0), (250, 100)),
        text='White: ' + str(white_timer),
        manager=self.manager)
    self.black_clock = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((560, 100), (250, 100)),
        text='Black: ' + str(black_timer),
        manager=self.manager)

def game_over_screen(self, winner):
    self.winner = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((560, 200), (250, 50)),
        text='Winner: ' + str(winner),
        manager=self.manager)
    self.start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((625, 275), (120, 50)),
        text='Restart Game',
        manager=self.manager)
