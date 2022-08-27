class Invoke:
    def __init__(self, move, board):
        self.gm = board.gm
        self.board = board
        self.move = move
        self.type = self.move.type
        self.current_sq = self.move.current_sq
        self.piece = self.current_sq.piece
        self.target_sq = self.move.target_sq

    def forward(self):
        self.piece.square = self.target_sq
        self.piece.dragging = False
        self.piece.rect.center = self.target_sq.rect.center
        self.piece.already_moved = True
        self.board.sound.play()
        if self.type == "kill":
            self.target_sq.piece.kill()
        if self.type == "check":
            self.target_sq.piece.kill()
            self.gm.game_over(self.piece.color)
        else:
            # board update and turn switch
            self.board.run()
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
