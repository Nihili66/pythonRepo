from move import Move

class MoveGenerator:
    def __init__(self, board, player):
        self.legal_moves = []
        self.board = board
        self.player = player

    def generate_allowed_moves(self):
        for piece in self.board.pieces:
            if piece.color == self.player.color:
                sq_i = self.board.square_list.index(piece.square)
                if piece.move_type == "sliding":
                    sliding_gen(self.board, piece, sq_i, self.legal_moves)
                elif piece.move_type == "normal":
                    normal_gen(self.board, piece, sq_i, self.legal_moves)


def normal_gen(board, sprite, current_sq_i, allowed_moves):
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
                        allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
                    elif not board.square_list[target_sq_i].piece and move not in sprite.moves[-2:]:
                        allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
            elif sprite.type == "knight":
                target_y = int(target_sq_i / 8)
                target_x = int(target_sq_i - target_y * 8)
                max_move = max(abs(x - target_x), abs(y - target_y))
                if max_move == 2:
                    if board.square_list[target_sq_i].piece and board.square_list[
                        target_sq_i].piece.color != sprite.color:
                        allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
                    elif not board.square_list[target_sq_i].piece:
                        allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
            elif sprite.type == "king":
                target_y = int(target_sq_i / 8)
                target_x = int(target_sq_i - target_y * 8)
                max_move = max(abs(x - target_x), abs(y - target_y))
                if max_move <= 2:
                    if board.square_list[target_sq_i].piece and board.square_list[
                        target_sq_i].piece.color != sprite.color:
                        allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
                    elif not board.square_list[target_sq_i].piece:
                        allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))


def sliding_gen(board, sprite, current_sq_i, allowed_moves):
    move_offsets = sprite.moves
    x = 4 if sprite.type == "bishop" else 0
    y = 4 if sprite.type == "rook" else None
    for direction_index, direction in enumerate(board.square_to_edges[current_sq_i][x:y]):
        for number in range(1, direction + 1):
            target_sq_i = current_sq_i + number * move_offsets[x:y][direction_index]
            if board.square_list[target_sq_i].piece:
                if board.square_list[target_sq_i].piece.color != sprite.color:
                    allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
                    break
                elif board.square_list[target_sq_i].piece.color == sprite.color:
                    break
            else:
                allowed_moves.append(Move(board.square_list[current_sq_i], board.square_list[target_sq_i]))
