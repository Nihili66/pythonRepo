import pygame
from settings import *
from sprites import Player
from board import Board

class GManager:
    def __init__(self):
        # player setup
        self.whiteP = None
        self.blackP = None
        # board setup
        self.board = None

    def game_init(self, player1, player2):
        self.board = Board()
        self.whiteP = Player("white", player1, self.board)
        self.blackP = Player("black", player2, self.board)
        self.board.run()
        self.board.players.append(self.whiteP)
        self.board.players.append(self.blackP)

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

    def update(self):
        if self.board:
            self.board.run()
