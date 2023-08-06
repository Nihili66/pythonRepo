import pygame
from settings import *
from sprites import *


class Board:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.square_list = list(range(64))
        # sprite creation
        self.create_board()
        self.create_pieces()

    def create_board(self):
        for rank in range(8):
            for file in range(8):
                is_light = (rank + file) % 2 == 0
                color = (245, 210, 154) if is_light else (110, 77, 26)
                x = file * TILESIZE
                y = rank * TILESIZE
                self.square_list[file + (rank * 8)] = Tile(color, (x, y), [self.visible_sprites])

    def create_pieces(self):
        for square in self.square_list:
            if square.color == (245, 210, 154):
                if square.rect.y < 3 * TILESIZE:
                    Piece(square, [self.visible_sprites], "black/pawn")
                elif square.rect.y > 4 * TILESIZE:
                    Piece(square, [self.visible_sprites], "white/pawn")

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
