from move import Move


class MoveGenerator:
    def __init__(self, board):
        self.legal_moves = []
        self.board = board
        self.players = self.board.players
        self.player = None
        self.player_moves = None
        self.enemy_moves = None
        self.checked = None
        self.checked_squares = None

    def get_player_turns(self):
        for player in self.players:
            if player.turn:
                self.player = player

    def generate_enemy_moves(self):
        allowed_moves = []
        for square_index, square in enumerate(self.board.square_list):
            piece = square.piece
            if piece and piece.color != self.player.color:
                sq_i = self.board.square_list.index(piece.square)
                if piece.move_type == "sliding":
                    allowed_moves += sliding_gen(self.board, piece, sq_i)
                elif piece.move_type == "normal":
                    allowed_moves += normal_gen(self.board, piece, sq_i)
        self.enemy_moves = allowed_moves

    def check_for_check(self):
        check_squares = []
        check = False
        for move in self.enemy_moves:
            if move.type == "check":
                check_squares += move.check_squares
                check = True
        self.checked = check
        self.checked_squares = check_squares

    def generate_allowed_moves(self):
        allowed_moves = []
        for square_index, square in enumerate(self.board.square_list):
            piece = square.piece
            if piece and piece.color == self.player.color:
                sq_i = square_index
                if piece.move_type == "sliding":
                    allowed_moves += sliding_gen(self.board, piece, sq_i)
                elif piece.move_type == "normal":
                    allowed_moves += normal_gen(self.board, piece, sq_i)
        self.player_moves = allowed_moves

    def generate_legal_moves(self):
        legal_moves = []
        for move in self.player_moves:
            if self.checked:
                if move.current_sq.piece.type == "king":
                    if move.target_sq not in self.checked_squares and not move.target_sq.piece:
                        legal_moves.append(move)
                    elif move.target_sq in self.checked_squares and move.target_sq.piece:
                        legal_moves.append(move)
                elif move.target_sq in self.checked_squares and move.current_sq.piece.type != "king":
                    legal_moves.append(move)
            elif not self.checked:
                legal_moves.append(move)
        self.legal_moves = legal_moves

    def get_legal_moves(self):
        self.get_player_turns()
        self.generate_allowed_moves()
        self.generate_enemy_moves()
        self.check_for_check()
        self.generate_legal_moves()
        return self.legal_moves


def normal_gen(board, sprite, current_sq_i):
    allowed_moves = []
    y = int(current_sq_i / 8)
    x = int(current_sq_i - y * 8)
    for move in sprite.moves:
        target_sq_i = current_sq_i + move
        if 64 > target_sq_i >= 0:
            target_y = int(target_sq_i / 8)
            target_x = int(target_sq_i - target_y * 8)
            max_move = max(abs(x - target_x), abs(y - target_y))
            if sprite.type == "pawn":
                if max_move <= 2:
                    if board.square_list[target_sq_i].piece:
                        if board.square_list[target_sq_i].piece.color != sprite.color:
                            if move in sprite.moves[:2]:
                                allowed_moves.append(
                                    Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
                        else:
                            if move not in sprite.moves[:2]:
                                break
                    else:
                        if move not in sprite.moves[:2]:
                            allowed_moves.append(
                                Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
            elif sprite.type == "knight":
                if max_move == 2:
                    if board.square_list[target_sq_i].piece and board.square_list[
                        target_sq_i].piece.color != sprite.color:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
                    elif not board.square_list[target_sq_i].piece:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
            elif sprite.type == "king":
                if max_move <= 2:
                    if board.square_list[target_sq_i].piece and board.square_list[
                        target_sq_i].piece.color != sprite.color:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
                    elif not board.square_list[target_sq_i].piece:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
    return allowed_moves


def sliding_gen(board, sprite, current_sq_i):
    allowed_moves = []
    move_offsets = [8, -8, -1, 1, 7, -7, 9, -9]
    x = 4 if sprite.type == "bishop" else 0
    y = 4 if sprite.type == "rook" else None
    for direction_index, direction in enumerate(board.square_to_edges[current_sq_i][x:y]):
        for number in range(1, direction + 1):
            target_sq_i = current_sq_i + number * move_offsets[x:y][direction_index]
            if board.square_list[target_sq_i].piece:
                if board.square_list[target_sq_i].piece.color != sprite.color:
                    allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
                    break
                elif board.square_list[target_sq_i].piece.color == sprite.color:
                    break
            else:
                allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
    return allowed_moves
