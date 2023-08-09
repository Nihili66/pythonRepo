import pygame
from settings import *
from sprites import *


class Board:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.square_list = list(range(64))
        self.piece_list = []
        self.players = []
        # sprite creation
        self.cursor = Cursor()
        self.create_board()
        self.create_pieces()

    def create_board(self):
        for rank in range(8):
            for file in range(8):
                is_light = (rank + file) % 2 == 0
                color = (245, 210, 154) if is_light else (110, 77, 26)
                x = file * TILESIZE
                y = rank * TILESIZE
                self.square_list[file + (rank * 8)] = Tile(color, (x, y), [self.visible_sprites], self.piece_list)

    def create_pieces(self):
        for square in self.square_list:
            if square.color == (245, 210, 154):
                if square.rect.y < 3 * TILESIZE:
                    self.piece_list.append(Piece(square, [self.visible_sprites], "black/pawn"))
                elif square.rect.y > 4 * TILESIZE:
                    self.piece_list.append(Piece(square, [self.visible_sprites], "white/pawn"))
        for square in self.square_list:
            square.piece = square.check_for_piece()

    def run(self):
        self.cursor.update()
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
