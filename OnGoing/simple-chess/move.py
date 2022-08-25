class Move:
    def __init__(self, current_sq, target_sq):
        self.current_sq = current_sq
        self.target_sq = target_sq
        self.type = self.get_move_type()

    def get_move_type(self):
        if not self.target_sq.piece:
            return "normal"
        elif self.target_sq.piece.color != self.current_sq.piece.color:
            return "kill"
