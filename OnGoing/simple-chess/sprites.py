import pygame
from settings import TILESIZE, piece_moves

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, 12, 20)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.x = mx
        self.rect.y = my


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color, piece_list):
        super().__init__(groups)
        # setup
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.piece_list = piece_list
        self.piece = None

    def check_for_piece(self):
        for sprite in self.piece_list:
            if sprite.square == self:
                return sprite
        return None

    def update(self):
        self.piece = self.check_for_piece()

class Piece(pygame.sprite.Sprite):
    def __init__(self, square, groups, piece):
        super().__init__(groups)
        # setup
        self.name = piece
        self.color = piece.split("/")[0]
        self.type = piece.split("/")[1]
        self.image = pygame.image.load('./pieces/' + piece + ".png")
        self.rect = self.image.get_rect(center=square.rect.center)
        self.already_moved = False
        self.dragging = False
        self.square = square
        self.moves = []

    def gen_moves(self):
        if self.type == "pawn" and self.color == "white":
            if self.already_moved:
                return [[-8]]
            elif not self.already_moved:
                return [[-8, -16]]
        elif self.type == "pawn" and self.color == "black":
            if self.already_moved:
                return [[8]]
            elif not self.already_moved:
                return [[8, 16]]
        elif self.type == "knight":
            return [[-17], [-15], [-10], [-6], [6], [10], [15], [17]]
        elif self.type == "king":
            return [[-1], [1],   # horizontal
                    [-8], [8],   # vertical
                    [-9], [9],  # diagonal
                    [-7], [7]]   # diagonal
        elif self.type == "rook":
            return [[-1, -2, -3, -4, -5, -6, -7], [1, 2, 3, 4, 5, 6, 7],                  # horizontal
                    [-8, -16, -24, -32, -40, -48, -56], [8, 16, 24, 32, 40, 48, 56]]      # vertical
        elif self.type == "bishop":
            return [[7, 14, 21, 28, 35, 42, 49], [-7, -14, -21, -28, -35, -42, -49],      # diagonal
                    [9, 18, 27, 36, 45, 54, 63],[-9, -18, -27, -36, -45, -54, -63]]       # diagonal
        elif self.type == "queen":
            return [[-1, -2, -3, -4, -5, -6, -7], [1, 2, 3, 4, 5, 6, 7],                  # horizontal
                    [-8, -16, -24, -32, -40, -48, -56], [8, 16, 24, 32, 40, 48, 56],      # vertical
                    [-7, -14, -21, -28, -35, -42, -49], [7, 14, 21, 28, 35, 42, 49],      # diagonal
                    [9, 18, 27, 36, 45, 54, 63],[-9, -18, -27, -36, -45, -54, -63]]       # diagonal

    def update(self):
        self.moves = self.gen_moves()
