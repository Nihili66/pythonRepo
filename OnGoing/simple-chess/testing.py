square_to_edges = []


move_offsets = [-17,-10, 15, 6, -15, -6, 17, 10,]

square_to_edges[sq_index] = [down, up, left, right, diag_downleft, diag_upright, diag_downright,
                                             diag_upleft]



def check_allowed_moves(board, sprite, sq):
    allowed_moves = []
    sq_i = board.square_list.index(sq)
    move_offsets = sprite.moves
    if sprite.move_type == "sliding":
        sliding_gen(board, sprite, sq_i, allowed_moves)
    elif sprite.move_type == "normal":
        normal_gen(board, sprite, sq_i, allowed_moves)
    return allowed_moves

def normal_gen(board, sprite, sq_i, allowed_moves):
    y = int(sq_i / 8)
    x = int(sq_i - y * 8)
    for move in sprite.moves:
        target_i = sq_i + move
        if 64 > target_i >= 0:
            if sprite.type == "pawn":
                if board.square_list[target_i].piece and board.square_list[target_i].piece.color != sprite.color and move in sprite.moves[-2:]:
                    allowed_moves.append(board.square_list[target_i])
                elif not board.square_list[target_i].piece:
                    allowed_moves.append(board.square_list[target_i])
            elif sprite.type == "knight":
                target_y = int(target_i / 8)
                target_x = int(target_i - target_y * 8)
                max_move = max((x - target_x), (y - target_y))
                if max_move == 2:
                    if board.square_list[target_i].piece and board.square_list[target_i].piece.color != sprite.color:
                        allowed_moves.append(board.square_list[target_i])
                    elif not board.square_list[target_i].piece:
                        allowed_moves.append(board.square_list[target_i])
            else:
                if board.square_list[target_i].piece and board.square_list[target_i].piece.color != sprite.color:
                    allowed_moves.append(board.square_list[target_i])
                elif not board.square_list[target_i].piece:
                    allowed_moves.append(board.square_list[target_i])


def sliding_gen(board, sprite, sq_i, allowed_moves):
    x = 0
    y = None
    if sprite.type == "rook":
        x = 0
        y = 4
    elif sprite.type == "bishop":
        x = 4
        y = None
    for direction_index, direction in enumerate(board.square_to_edges[sq_i][x:y]):
        for number in range(1, direction + 1):
            movement = sq_i + number * move_offsets[x:y][direction_index]
            if board.square_list[movement].piece:
                if board.square_list[movement].piece.color != sprite.color:
                    allowed_moves.append(board.square_list[movement])
                    break
                elif board.square_list[movement].piece.color == sprite.color:
                    break
            else:
                allowed_moves.append(board.square_list[movement])
