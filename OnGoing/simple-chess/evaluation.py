from piecesquaretables import table_dict

class Evaluate:
    def __init__(self, board):
        self.board = board
        self.pieces = board.pieces
        self.players = self.board.players
        self.player = None
        # values dict
        self.values = {
            "pawn": 100,
            "knight": 300,
            "bishop": 350,
            "rook": 500,
            "queen": 900,
            "king": 100000
        }
        # evaluation
        self.white_evaluation = 0
        self.black_evaluation = 0

    def evaluate_pieces(self):
        for piece in self.pieces:
            squaretable = table_dict.get(piece.type)
            sq_i = self.board.square_list.index(piece.square)
            y = sq_i // 8
            x = sq_i - (y * 8)
            if piece.color == "white":
                # self.white_evaluation += self.values[piece.type] * squaretable[y][x]
                self.white_evaluation += self.values[piece.type]
            elif piece.color == "black":
                # self.black_evaluation += self.values[piece.type] * squaretable[7 - y][x]
                self.black_evaluation += self.values[piece.type]

    def evaluate_board(self):
        self.evaluate_pieces()
        for player in self.players:
            if player.turn:
                self.player = player

        if self.player.color == "white":
            return self.white_evaluation - self.black_evaluation
        elif self.player.color == "black":
            return self.black_evaluation - self.white_evaluation



