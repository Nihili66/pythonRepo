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
                            target_piece = check_collision(sprite, board.pieces)
                            if square in allowed_moves:
                                if not target_piece:
                                    sprite.square = square
                                    sprite.rect.center = square.rect.center
                                    sprite.dragging = False
                                elif target_piece.color != sprite.color:
                                    target_piece.kill()
                                    sprite.square = square
                                    sprite.rect.center = square.rect.center
                                    sprite.dragging = False
                                elif target_piece.color == sprite.color:
                                    sprite.dragging = False
                                    sprite.rect.center = sq.rect.center
                            else:
                                sprite.dragging = False
                                sprite.rect.center = sq.rect.center

        elif event.type == pygame.MOUSEMOTION:
            if sprite.dragging:
                sprite.rect.center = board.cursor.rect.center


def check_collision(sprite, sprite_list):
    for target_sprite in sprite_list:
        if target_sprite != sprite and sprite.rect.colliderect(target_sprite.rect):
            return target_sprite
    return False


def check_allowed_moves(board, sprite, sq):
    allowed_moves = []
    sq_i = board.square_list.index(sq)
    for move in sprite.moves:
        try:
            allowed_moves.append(board.square_list[sq_i + move])
        except IndexError:
            pass
    return allowed_moves
