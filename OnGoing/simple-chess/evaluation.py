from piecesquaretables import SquareTable

class Evaluate:
    def __init__(self, board):
        self.board = board
        self.pieces = board.pieces
        self.players = self.board.players
        self.player = None
        # values dict
        self.values = {
            "pawn": 1,
            "knight": 3,
            "bishop": 3,
            "rook": 5,
            "queen": 9,
            "king": 1000
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
        for player in self.players:
            if player.turn:
                self.player = player

        if self.player.color == "white":
            return self.white_evaluation - self.black_evaluation
        elif self.player.color == "black":
            return self.black_evaluation - self.white_evaluation



