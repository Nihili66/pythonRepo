import pygame
from settings import TILESIZE
from movegenerator import MoveGenerator
# from invokemove import Invoke

class HumanMovement:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.movegenerator = None
        self.current_sq = None
        self.piece = None
        self.target_sq = None
        self.move = None
        self.allowed_moves = []

    def pick_move(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.current_sq = self.board.square_list[event.pos[1] // TILESIZE * 8 + event.pos[0] // TILESIZE]
                if self.current_sq.piece:
                    self.piece = self.current_sq.piece
                    if self.player.color == self.piece.color and self.player.turn:
                        self.piece.dragging = True
                        self.movegenerator = MoveGenerator(self.board)
                        self.allowed_moves = self.movegenerator.player_moves
                        hover_squares(self.allowed_moves, self.current_sq)

    def play_move(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.piece.dragging:
                self.piece.rect.center = self.board.cursor.rect.center
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.piece.dragging:
                    self.target_sq = self.board.square_list[event.pos[1] // TILESIZE * 8 + event.pos[0] // TILESIZE]
                    for move in self.allowed_moves:
                        if move.current_sq == self.current_sq and move.target_sq == self.target_sq:
                            self.move = move
                    if self.move:
                        self.movegenerator.move_invoke = self.move
                        self.movegenerator.forward()
                        self.move = None
                        hover_squares(self.allowed_moves, self.current_sq, False)
                    elif not self.move:
                        self.piece.dragging = False
                        self.piece.rect.center = self.piece.square.rect.center
                        hover_squares(self.allowed_moves, self.current_sq, False)

def hover_squares(legal_moves, current_sq, toggled=True):
    for move in legal_moves:
        if move.current_sq == current_sq:
            if toggled:
                move.target_sq.color = (255, 0, 0)
            else:
                move.target_sq.color = move.target_sq.original_color
