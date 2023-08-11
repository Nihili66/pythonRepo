class Move:
    def __init__(self, current_sq, target_sq, target_sq_i, board, offset):
        self.board = board
        self.current_sq = current_sq
        self.target_sq = target_sq
        self.target_sq_i = target_sq_i
        self.type = self.get_move_type()
        self.offset = offset

    def get_move_type(self):
        if not self.target_sq.piece:
            return "normal"
        elif self.target_sq.piece.color != self.current_sq.piece.color:
            return "kill"
