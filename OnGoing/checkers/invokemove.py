class Invoke:
    def __init__(self, move, board):
        self.gm = board.gm
        self.board = board
        self.move = move
        self.type = self.move.type
        self.offset = self.move.offset
        self.current_sq = self.move.current_sq
        self.piece = self.current_sq.piece
        self.target_sq = self.move.target_sq
        self.target_sq_i = self.move.target_sq_i
        self.target_piece = self.target_sq.piece

    def forward(self):
        self.current_sq.piece = None
        if self.type == "kill":
            self.target_sq.piece.kill()
            self.target_sq = self.board.square_list[self.target_sq_i + self.offset]
        self.target_sq.piece = self.piece
        self.piece.square = self.target_sq
        self.piece.dragging = False
        switch_turns(self.board)


def switch_turns(board):
    for player in board.players:
        if player.turn:
            player.turn = False
        else:
            player.turn = True
