import pygame
from settings import TILESIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, color, pos, groups):
        super().__init__(groups)
        # setup
        self.original_color = color
        self.color = self.original_color
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.rect = self.image.get_rect(topleft=pos)

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

    def update(self):
        self.rect.center = self.square.rect.center

