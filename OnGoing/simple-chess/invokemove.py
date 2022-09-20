class Invoke:
    def __init__(self, move, board):
        self.gm = board.gm
        self.board = board
        self.move = move
        self.type = self.move.type
        self.current_sq = self.move.current_sq
        self.piece = self.current_sq.piece
        self.target_sq = self.move.target_sq
        self.target_piece = self.target_sq.piece
        self.first_move = True if not self.piece.already_moved else False

    def forward(self):
        if self.type == "kill":
            self.target_sq.piece.kill()
        self.current_sq.piece = None
        self.target_sq.piece = self.piece
        self.piece.square = self.target_sq
        self.piece.dragging = False
        self.board.sound.play()
        if self.type == "check":
            self.target_sq.piece.kill()
            self.gm.game_over(self.piece.color)
        else:
            switch_turns(self.board)
        if self.first_move:
            self.piece.already_moved = True
            self.piece.moves = self.piece.gen_moves()


class ImaginaryInvoke:
    def __init__(self, move, board):
        # real move data
        self.move = move
        self.type = move.type
        self.real_current_sq = self.move.current_sq
        self.real_piece = self.real_current_sq.piece
        self.real_target_sq = self.move.target_sq
        # imaginary board data
        self.board = board
        self.square_list = self.board.square_list
        self.pieces = self.board.pieces
        # imaginary move data
        self.current_sq = self.square_list[self.move.board.square_list.index(self.real_current_sq)]
        self.piece = self.current_sq.piece
        self.target_sq = self.square_list[self.move.board.square_list.index(self.real_target_sq)]
        self.target_piece = self.target_sq.piece
        self.first_move = True if not self.piece.already_moved else False

    def forward(self):
        if self.type == "kill":
            self.pieces.remove(self.target_piece)
        if self.type == "check":
            self.pieces.remove(self.target_piece)
        self.current_sq.piece = None
        self.target_sq.piece = self.piece
        self.piece.square = self.target_sq
        if self.first_move:
            self.piece.already_moved = True
            self.piece.moves = self.piece.gen_moves()
        switch_turns(self.board)

    def backward(self):
        self.target_sq.piece = None
        self.current_sq.piece = self.piece
        self.piece.square = self.current_sq
        if self.type == "kill":
            self.board.pieces.append(self.target_piece)
            self.target_piece.square = self.target_sq
            self.target_sq.piece = self.target_piece
        if self.type == "check":
            self.board.pieces.append(self.target_piece)
            self.target_piece.square = self.target_sq
            self.target_sq.piece = self.target_piece
        if self.first_move:
            self.piece.already_moved = False
            self.piece.moves = self.piece.gen_moves()
        switch_turns(self.board)


def check_castling(board, sprite):
    if sprite.type == "king" and not sprite.already_moved:
        sq_i = board.square_list.index(sprite.square)
        if sprite.color == "white":
            rk_square = board.square_list[sq_i + 1]
            if rk_square.piece:
                if rk_square.piece.type == "rook" and not rk_square.piece.already_moved:
                    rk_square.piece.rect.center = board.square_list[sq_i - 1].rect.center
                    rk_square.piece.square = board.square_list[sq_i - 1]
                    rk_square.piece.already_moved = True
        elif sprite.color == "black":
            rk_square = board.square_list[sq_i - 1]
            if rk_square.piece:
                if rk_square.piece.type == "rook" and not rk_square.piece.already_moved:
                    rk_square.piece.rect.center = board.square_list[sq_i + 1].rect.center
                    rk_square.piece.square = board.square_list[sq_i + 1]
                    rk_square.piece.already_moved = True

def switch_turns(board):
    for player in board.players:
        if player.turn:
            player.turn = False
        else:
            player.turn = True
