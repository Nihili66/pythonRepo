class Evaluate:
    def __init__(self, board, player):
        self.board = board
        self.pieces = board.pieces
        self.player = player
        # piece values
        self.pawn_value = 1
        self.knight_value = 3
        self.bishop_value = 3
        self.rook_value = 5
        self.queen_value = 9
        self.king_value = 1000
        # values dict
        self.values = {
            "pawn": self.pawn_value,
            "knight": self.knight_value,
            "bishop": self.bishop_value,
            "rook": self.rook_value,
            "queen": self.queen_value,
            "king": self.king_value
        }
        # evaluation
        self.white_evaluation = 0
        self.black_evaluation = 0

    def evaluate_pieces(self):
        for piece in self.pieces:
            if piece.color == "white":
                self.white_evaluation += self.values[piece.type]
            elif piece.color == "black":
                self.black_evaluation += self.values[piece.type]

    def evaluate_board(self):
        self.evaluate_pieces()
        if self.player.color == "white":
            return self.white_evaluation - self.black_evaluation
        elif self.player.color == "black":
            return self.black_evaluation - self.white_evaluation



