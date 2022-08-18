from settings import TILESIZE


class MovementLogic:
    def __init__(self, board):
        self.board = board
        self.current_sq = None
        self.piece = None
        self.target_sq = None
        self.allowed_moves = []
        self.move = []

    def clicking(self, event):
        self.current_sq = self.board.square_list[event.pos[1] // TILESIZE * 8 + event.pos[0] // TILESIZE]
        if self.current_sq.piece:
            self.piece = self.current_sq.piece
            for player in self.board.players:
                if player.color == self.piece.color and player.turn:
                    self.piece.dragging = True
                    self.allowed_moves = check_allowed_moves(self.board, self.piece, self.current_sq)
                    hover_squares(self.allowed_moves)

    def putting(self, event):
        if self.piece.dragging:
            self.target_sq = self.board.square_list[event.pos[1] // TILESIZE * 8 + event.pos[0] // TILESIZE]
            if self.target_sq in self.allowed_moves:
                if not self.target_sq.piece:
                    move_piece("normal", self.piece, self.target_sq, self.board)
                    hover_squares(self.allowed_moves, False)
                else:
                    move_piece("kill", self.piece, self.target_sq, self.board)
                    hover_squares(self.allowed_moves, False)
            else:
                move_piece("cancel", self.piece, self.current_sq, self.board)
                hover_squares(self.allowed_moves, False)

    def dragging(self):
        if self.piece.dragging:
            self.piece.rect.center = self.board.cursor.rect.center


def hover_squares(squares, toggled=True):
    for square in squares:
        if toggled:
            square.color = (255, 0, 0)
        else:
            square.color = square.original_color


def check_allowed_moves(board, sprite, sq):
    allowed_moves = []
    sq_i = board.square_list.index(sq)
    for direction in sprite.moves:
        for move in direction:
            movement = sq_i + move
            if 64 > movement >= 0:
                try:
                    if board.square_list[movement].piece:
                        if board.square_list[movement].piece.color != sprite.color:
                            allowed_moves.append(board.square_list[movement])
                            break
                        elif board.square_list[movement].piece.color == sprite.color:
                            break
                    else:
                        allowed_moves.append(board.square_list[movement])
                except IndexError:
                    pass
    return allowed_moves

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

def move_piece(move_type, sprite, target_sq, board):
    if move_type == "normal":
        sprite.rect.center = target_sq.rect.center
        sprite.dragging = False
        sprite.square = target_sq
        check_castling(board, sprite)
        sprite.already_moved = True
        switch_turns(board)
    elif move_type == "kill":
        target_sq.piece.kill()
        sprite.rect.center = target_sq.rect.center
        sprite.dragging = False
        sprite.square = target_sq
        sprite.already_moved = True
        switch_turns(board)
    elif move_type == "cancel":
        sprite.dragging = False
        sprite.rect.center = sprite.square.rect.center
