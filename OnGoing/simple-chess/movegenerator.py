from move import Move


class MoveGenerator:
    def __init__(self, board, player):
        self.legal_moves = []
        self.board = board
        self.player = player
        self.player_moves = None
        self.enemy_moves = None
        self.checked = None
        self.checked_squares = None


    def generate_enemy_moves(self):
        allowed_moves = []
        for piece in self.board.pieces:
            if piece:
                if piece.color != self.player.color:
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
        for piece in self.board.pieces:
            if piece:
                if piece.color == self.player.color:
                    sq_i = self.board.square_list.index(piece.square)
                    if piece.move_type == "sliding":
                        allowed_moves += sliding_gen(self.board, piece, sq_i)
                    elif piece.move_type == "normal":
                        allowed_moves += normal_gen(self.board, piece, sq_i)
        self.player_moves = allowed_moves

    def generate_legal_moves(self):
        legal_moves = []
        for enemy_move in self.enemy_moves:
            for move in self.player_moves:
                if move.current_sq.piece.type == "king" and move.target_sq == enemy_move.target_sq:
                    break
                if self.checked:
                    if move.current_sq.piece.type == "king" and move.target_sq not in self.checked_squares:
                        legal_moves.append(move)
                    elif move.target_sq in self.checked_squares and move.current_sq.piece.type != "king":
                        legal_moves.append(move)
                elif not self.checked:
                    legal_moves.append(move)
        self.legal_moves = legal_moves

    def get_legal_moves(self):
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
            if sprite.type == "pawn":
                target_y = int(target_sq_i / 8)
                target_x = int(target_sq_i - target_y * 8)
                max_move = max(abs(x - target_x), abs(y - target_y))
                if max_move <= 2:
                    if board.square_list[target_sq_i].piece and board.square_list[
                        target_sq_i].piece.color != sprite.color and move in sprite.moves[-2:]:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
                    elif not board.square_list[target_sq_i].piece and move not in sprite.moves[-2:]:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
            elif sprite.type == "knight":
                target_y = int(target_sq_i / 8)
                target_x = int(target_sq_i - target_y * 8)
                max_move = max(abs(x - target_x), abs(y - target_y))
                if max_move == 2:
                    if board.square_list[target_sq_i].piece and board.square_list[
                        target_sq_i].piece.color != sprite.color:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
                    elif not board.square_list[target_sq_i].piece:
                        allowed_moves.append(
                            Move(board.square_list[current_sq_i], board.square_list[target_sq_i], board))
            elif sprite.type == "king":
                target_y = int(target_sq_i / 8)
                target_x = int(target_sq_i - target_y * 8)
                max_move = max(abs(x - target_x), abs(y - target_y))
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
