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

# square position enumeration
squares = []
for row_index, row in enumerate(BOARD_MAP):
    for col_index, col in enumerate(row):
        x = col_index * TILESIZE
        y = row_index * TILESIZE
        squares.append((x, y))

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
