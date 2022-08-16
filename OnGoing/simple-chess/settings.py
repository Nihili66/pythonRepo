# screen settings
FPS = 60
TILESIZE = 70
WIDTH = 8 * TILESIZE
HEIGTH = 8 * TILESIZE

# board squares
BOARD_MAP = [
    ['x', 'y', 'x', 'y', 'x', 'y', 'x', 'y'],
    ['y', 'x', 'y', 'x', 'y', 'x', 'y', 'x'],
    ['x', 'y', 'x', 'y', 'x', 'y', 'x', 'y'],
    ['y', 'x', 'y', 'x', 'y', 'x', 'y', 'x'],
    ['x', 'y', 'x', 'y', 'x', 'y', 'x', 'y'],
    ['y', 'x', 'y', 'x', 'y', 'x', 'y', 'x'],
    ['x', 'y', 'x', 'y', 'x', 'y', 'x', 'y'],
    ['y', 'x', 'y', 'x', 'y', 'x', 'y', 'x'],
]

# fen characters dictionnary
fen_dict = {
    'r': "black/rook",
    'n': "black/knight",
    'b': "black/bishop",
    'q': "black/queen",
    'k': "black/king",
    'p': "black/pawn",
    'R': "white/rook",
    'N': "white/knight",
    'B': "white/bishop",
    'Q': "white/queen",
    'K': "white/king",
    'P': "white/pawn",
}

# piece moves dictionnary
piece_moves = {
    "pawn": [(8, 16), (-8, -16)],
    "knight": [(-17, -15, -10, -6, 6, 10, 15, 17)],
    "king": [(-1, 1, -8, 8, -9, 9, -7, 7)],
    "rook": [(-1, 1, -8, 8)],
    "bishop": [(-9, 9, -7, 7)],
    "queen": [(-1, 1, -8, 8, -9, 9, -7, 7)]
}

