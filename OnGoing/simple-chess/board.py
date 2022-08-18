import pygame
from settings import *
from sprites import Player, Tile, Piece, Cursor

class Board:
    def __init__(self, fen):
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        self.players = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()
        self.square_list = list(range(64))
        # sprite creation
        self.create_board()
        self.create_pieces(fen)
        self.init_players()

    def init_players(self):
        Player("white", [self.players])
        Player("black", [self.players])

    def create_board(self):
        for file in range(8):
            for rank in range(8):
                is_light = (file + rank) % 2 == 0
                color = (245, 210, 154) if is_light else (110, 77, 26)
                x = rank * TILESIZE
                y = file * TILESIZE
                self.square_list[rank + (file * 8)] = Tile((x, y), [self.visible_sprites], color, self.pieces)

    def create_pieces(self, fen):
        self.cursor = Cursor()
        fen_list = []
        for char in fen:
            if char == "/":
                pass
            elif not char.isnumeric():
                fen_list.append(char)
            else:
                for i in range(int(char)):
                    fen_list.append("x")
        for field_index, field in enumerate(fen_list):
            if field == "x":
                pass
            else:
                Piece(self.square_list[field_index], [self.visible_sprites, self.pieces], fen_dict.get(field))

    def run(self):
        self.cursor.update()
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
