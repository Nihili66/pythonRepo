import pygame

def move_piece(board, event):
    for sprite in board.pieces:
        sq = sprite.square
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if sprite.rect.colliderect(board.cursor.rect):
                    sprite.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if sprite.dragging:
                    allowed_moves = check_allowed_moves(board, sprite, sq)
                    for square in board.square_list:
                        if square.rect.colliderect(board.cursor.rect):
                            if square in allowed_moves:
                                if not square.piece:
                                    sprite.rect.center = square.rect.center
                                    sprite.dragging = False
                                    sprite.square = square
                                    sprite.already_moved = True
                                else:
                                    square.piece.kill()
                                    sprite.rect.center = square.rect.center
                                    sprite.dragging = False
                                    sprite.square = square
                                    sprite.already_moved = True
                            else:
                                sprite.dragging = False
                                sprite.rect.center = sq.rect.center

        elif event.type == pygame.MOUSEMOTION:
            if sprite.dragging:
                sprite.rect.center = board.cursor.rect.center


def check_allowed_moves(board, sprite, sq):
    allowed_moves = []
    sq_i = board.square_list.index(sq)
    move_list = sprite.moves
    for direction in sprite.moves:
        for move in direction:
            try:
                if board.square_list[sq_i + move].piece:
                    if board.square_list[sq_i + move].piece.color != sprite.color:
                        allowed_moves.append(board.square_list[sq_i + move])
                        break
                    elif board.square_list[sq_i + move].piece.color == sprite.color:
                        break
                else:
                    allowed_moves.append(board.square_list[sq_i + move])
            except IndexError:
                pass
    return allowed_moves
