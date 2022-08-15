pawn_moves

def get_current_sq(sprite):
    sq = None
    for square_index, square in square_list:
        if sprite.rect.center = square.rect.center
        sq = square_index
    return sq

if sprite.name == "white/pawn":
    allowed_moves = []
    allowed_moves.append(square_list[get_current_sq() - 8])

