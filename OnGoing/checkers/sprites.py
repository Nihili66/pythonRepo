import pygame
from settings import TILESIZE
from human import HumanMovement


class Player(pygame.sprite.Sprite):
    def __init__(self, color, genre, board):
        super().__init__()
        self.board = board
        self.color = color
        self.turn = True if self.color == "white" else False
        self.type = genre
        self.movement = HumanMovement(self.board, self)


class Tile(pygame.sprite.Sprite):
    def __init__(self, color, pos, groups, piece_list):
        super().__init__(groups)
        # setup
        self.original_color = color
        self.color = self.original_color
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.rect = self.image.get_rect(topleft=pos)
        self.piece_list = piece_list
        self.piece = None

    def check_for_piece(self):
        for sprite in self.piece_list:
            if sprite.square == self:
                return sprite
        return None

    def update(self):
        self.image.fill(self.color)


class Piece(pygame.sprite.Sprite):
    def __init__(self, square, groups, piece):
        super().__init__(groups)
        # setup
        self.name = piece
        self.color = piece.split("/")[0]
        self.type = piece.split("/")[1]
        self.square = square
        self.image = pygame.image.load('./pieces/' + piece + ".png")
        self.rect = self.image.get_rect(center=square.rect.center)
        self.dragging = False

    def gen_moves(self):
        if self.color == "white":
            return [-9, -7]
        else:
            return [9, 7]

    def update(self):
        if not self.dragging:
            self.rect.center = self.square.rect.center


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, 10, 10)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.x = mx
        self.rect.y = my

