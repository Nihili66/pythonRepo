import pygame
from settings import TILESIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, color, groups):
        super().__init__(groups)
        self.color = color
        self.turn = self.init_turns()

    def init_turns(self):
        if self.color == "white":
            return True
        elif self.color == "black":
            return False

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, 10, 10)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.x = mx
        self.rect.y = my


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color, piece_list):
        super().__init__(groups)
        # setup
        self.original_color = color
        self.color = self.original_color
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.rect = self.image.get_rect(topleft=pos)
        # pieces
        self.piece_list = piece_list
        self.piece = None

    def check_for_piece(self):
        for sprite in self.piece_list:
            if sprite.square == self:
                return sprite
        return None

    def update(self):
        self.piece = self.check_for_piece()
        self.image.fill(self.color)

class Piece(pygame.sprite.Sprite):
    def __init__(self, square, groups, piece, move):
        super().__init__(groups)
        # setup
        self.name = piece
        self.color = piece.split("/")[0]
        self.type = piece.split("/")[1]
        self.move_type = move
        self.image = pygame.image.load('./pieces/' + piece + ".png")
        self.rect = self.image.get_rect(center=square.rect.center)
        self.already_moved = False
        self.dragging = False
        self.square = square
        self.moves = []

    def gen_moves(self):
        if self.type == "pawn" and self.color == "white":
            if self.already_moved:
                return [-8]
            elif not self.already_moved:
                return [-8, -16]
        elif self.type == "pawn" and self.color == "black":
            if self.already_moved:
                return [8]
            elif not self.already_moved:
                return [8, 16]
        elif self.type == "knight":
            return [-17, -15, -10, -6, 6, 10, 15, 17]
        elif self.type == "king":
            if not self.already_moved:
                return [-1, -2, 1, 2, -8, 8, -9, 9, -7, 7]
            elif self.already_moved:
                return [-1, 1, -8, 8, -9, 9, -7, 7]
        elif self.type == "rook":
            return [8, -8, -1, 1, 7, -7, 9, -9]
        elif self.type == "bishop":
            return [8, -8, -1, 1, 7, -7, 9, -9]
        elif self.type == "queen":
            return [8, -8, -1, 1, 7, -7, 9, -9]

    def update(self):
        self.moves = self.gen_moves()
