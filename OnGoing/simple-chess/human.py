from settings import TILESIZE
from movegenerator import MoveGenerator


class HumanMovement:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.movegenerator = None
        self.current_sq = None
        self.piece = None
        self.target_sq = None
        self.allowed_moves = []

    def clicking(self, event):
        self.current_sq = self.board.square_list[event.pos[1] // TILESIZE * 8 + event.pos[0] // TILESIZE]
        if self.current_sq.piece:
            self.piece = self.current_sq.piece
            if self.player.color == self.piece.color and self.player.turn:
                self.piece.dragging = True
                self.movegenerator = MoveGenerator(self.board, self.player)
                self.movegenerator.generate_allowed_moves()
                self.allowed_moves = self.movegenerator.legal_moves
                hover_squares(self.allowed_moves, self.current_sq)

    def putting(self, event):
        if self.piece.dragging:
            self.target_sq = self.board.square_list[event.pos[1] // TILESIZE * 8 + event.pos[0] // TILESIZE]
            for move in self.allowed_moves:
                if move.current_sq == self.current_sq and move.target_sq == self.target_sq:
                    if not self.target_sq.piece:
                        move_piece("normal", self.piece, self.target_sq, self.board)
                        hover_squares(self.allowed_moves, self.current_sq, False)
                    else:
                        move_piece("kill", self.piece, self.target_sq, self.board)
                        hover_squares(self.allowed_moves, self.current_sq, False)
                else:
                    move_piece("cancel", self.piece, self.current_sq, self.board)
                    hover_squares(self.allowed_moves, self.current_sq, False)

    def dragging(self):
        if self.piece.dragging:
            self.piece.rect.center = self.board.cursor.rect.center


def hover_squares(legal_moves, current_sq, toggled=True):
    for move in legal_moves:
        if move.current_sq == current_sq:
            if toggled:
                move.target_sq.color = (255, 0, 0)
            else:
                move.target_sq.color = move.target_sq.original_color

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
