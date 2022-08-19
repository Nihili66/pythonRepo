square_to_edges = []


move_offsets = [8, -8, -1, 1, 7, -7, 9, -9]

if self.type == "rook":
    move_offsets[:4]
    square_to_edges[sq_i][:4]
elif self.type == "bishop":
    move_offsets[4:]
    square_to_edges[sq_i][4:]
elif self.type == "queen":
    move_offsets
    square_to_edges[sq_i]

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
    for move in sprite.moves:
        movement = sq_i + move
        if 64 > movement >= 0:
            if board.square_list[movement].piece:
                if board.square_list[movement].piece.color != sprite.color:
                    allowed_moves.append(board.square_list[movement])
                    break
                elif board.square_list[movement].piece.color == sprite.color:
                    break
            else:
                allowed_moves.append(board.square_list[movement])

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
