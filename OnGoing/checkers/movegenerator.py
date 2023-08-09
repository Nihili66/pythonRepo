from move import Move

class MoveGenerator:
    def __init__(self, board):
        self.legal_moves = []
        self.board = board
        self.players = self.board.players
        self.player = None
        self.player_moves = None
        self.get_player_turns()
        self.generate_player_moves()

    def get_player_turns(self):
        for player in self.players:
            if player.turn:
                self.player = player

    def generate_player_moves(self):
        allowed_moves = []
        for square_index, square in enumerate(self.board.square_list):
            piece = square.piece
            if piece and piece.color == self.player.color:
                sq_i = square_index
                if piece.type == "pawn":
                    allowed_moves += pawn_gen(self.board, piece, sq_i)
        self.player_moves = allowed_moves


def pawn_gen(board, sprite, current_sq_i):
    allowed_moves = []
    offset = sprite.gen_moves()
    for move in offset:
        target_sq_i = current_sq_i + move
        if target_sq_i in range(64):
            target_sq = board.square_list[target_sq_i]
            if not target_sq.piece:
                allowed_moves.append(Move(sprite.square, target_sq, board))
            elif target_sq.piece.color != sprite.color:
                allowed_moves.append(Move(sprite.square, target_sq, board))
    return allowed_moves


