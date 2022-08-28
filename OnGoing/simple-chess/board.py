import pygame
from settings import *
from sprites import Player, Tile, Piece, Cursor

class Board:
    def __init__(self, fen, manager):
        self.gm = manager
        self.display_surface = pygame.display.get_surface()
        self.sound = pygame.mixer.Sound("./pieces/click.wav")
        # sprite groups
        self.players = []
        self.visible_sprites = pygame.sprite.Group()
        self.pieces = []
        self.square_list = list(range(64))
        self.square_to_edges = list(range(64))
        # sprite creation
        self.create_board()
        self.create_pieces(fen)
        self.get_squares_to_edges()

    def create_board(self):
        for rank in range(8):
            for file in range(8):
                is_light = (rank + file) % 2 == 0
                color = (245, 210, 154) if is_light else (110, 77, 26)
                x = file * TILESIZE
                y = rank * TILESIZE
                self.square_list[file + (rank * 8)] = Tile((x, y), [self.visible_sprites], color, self.pieces)

    def get_squares_to_edges(self):
        for rank in range(8):
            for file in range(8):
                down = 7 - rank
                up = rank
                left = file
                right = 7 - file
                diag_upleft = min(up, left)
                diag_upright = min(up, right)
                diag_downleft = min(down, left)
                diag_downright = min(down, right)

                sq_index = file + (rank * 8)

                self.square_to_edges[sq_index] = [down, up, left, right, diag_downleft, diag_upright, diag_downright,
                                             diag_upleft]

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
               self.pieces.append(Piece(self.square_list[field_index], [self.visible_sprites], fen_dict.get(field)[0], fen_dict.get(field)[1]))

    def run(self):
        self.cursor.update()
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
