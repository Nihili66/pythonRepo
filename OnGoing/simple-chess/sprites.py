import pygame
from settings import TILESIZE

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, 12, 20)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.x = mx
        self.rect.y = my


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color):
        super().__init__(groups)
        # setup
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


class Piece(pygame.sprite.Sprite):
    def __init__(self, square, groups, piece):
        super().__init__(groups)
        # setup
        self.color = piece.split("/")[0]
        self.type = piece.split("/")[1]
        self.image = pygame.image.load('./pieces/' + piece + ".png")
        self.rect = self.image.get_rect(center=square.rect.center)
        self.dragging = False
        self.square = square
        self.moves = self.gen_moves()

    def gen_moves(self):
        if self.type == "pawn" and self.color == "white":
            return [-8, -16]
        elif self.type == "pawn" and self.color == "black":
            return [8, 16]
        elif self.type == "knight":
            return [-17, -15, -10, -6, 6, 10, 15, 17]
        elif self.type == "rook":
            return [-1, -2, -3, -4, -5, -6, -7, 1, 2, 3, 4, 5, 6, 7,
                    -8, -16, -24, -32, -40, -48, -56, 8, 16, 24, 32, 40, 48, 56]
        elif self.type == "bishop":
            return [7, 14, 21, 28, 35, 42, 49, -7, -14, -21, -28, -35, -42, -49,
                    9, 18, 27, 36, 45, 54, 63,-9, -18, -27, -36, -45, -54, -63]
        elif self.type == "queen":
            return [-1, -2, -3, -4, -5, -6, -7, 1, 2, 3, 4, 5, 6, 7,
                    -8, -16, -24, -32, -40, -48, -56, 8, 16, 24, 32, 40, 48, 56,
                    -7, -14, -21, -28, -35, -42, -49, 7, 14, 21, 28, 35, 42, 49,
                    9, 18, 27, 36, 45, 54, 63,-9, -18, -27, -36, -45, -54, -63]
        elif self.type == "king":
            return [-1, 1,
                    -8, 8,
                    -9, 9
                    -7, 7]

