import random

from movegenerator import MoveGenerator

class AiMovement:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.movegenerator = None
        self.allowed_moves = None
        self.current_sq = None
        self.piece = None
        self.target_sq = None

    def pick_random_move(self):
        self.movegenerator = MoveGenerator(self.board, self.player)
        self.movegenerator.generate_allowed_moves()
        self.allowed_moves = self.movegenerator.legal_moves
        move = random.choice(self.allowed_moves)
        self.current_sq = move.current_sq
        self.piece = move.current_sq.piece
        self.target_sq = move.target_sq

    def invoke_move(self):
        if not self.target_sq.piece:
            move_piece("normal", self.piece, self.target_sq, self.board)
        else:
            move_piece("kill", self.piece, self.target_sq, self.board)

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
