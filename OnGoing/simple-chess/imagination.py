class ImaginaryTile:
    def __init__(self, color, piece_list):
        self.color = color
        # pieces
        self.piece_list = piece_list
        self.piece = None

    def check_for_piece(self):
        for sprite in self.piece_list:
            if sprite.square == self:
                return sprite
        return None


class ImaginaryPiece:
    def __init__(self, square, piece, move):
        self.name = piece
        self.color = piece.split("/")[0]
        self.type = piece.split("/")[1]
        self.move_type = move
        self.square = square
        self.already_moved = False
        self.dragging = False
        self.moves = self.gen_moves()

    def gen_moves(self):
        if self.type == "pawn" and self.color == "white":
            if self.already_moved:
                return [-8, -7, -9]
            elif not self.already_moved:
                return [-8, -16, -7, -9]
        elif self.type == "pawn" and self.color == "black":
            if self.already_moved:
                return [8, 7, 9]
            elif not self.already_moved:
                return [8, 16, 7, 9]
        elif self.type == "knight":
            return [-17, -15, -10, -6, 6, 10, 15, 17]
        elif self.type == "king":
            return [-1, 1, -8, 8, -9, 9, -7, 7]


class ImaginaryBoard:
    def __init__(self, board):
        # real board data
        self.real_board = board
        real_square_list = self.real_board.square_list
        real_players = self.real_board.players
        real_pieces = self.real_board.pieces
        # imaginary board data
        self.square_list = []
        self.players = real_players
        self.pieces = []
        self.square_to_edges = self.real_board.square_to_edges
        # initialize imaginary board and pieces
        self.create_imaginary_board(real_square_list)
        self.create_imaginary_pieces(real_pieces, real_square_list)

    def create_imaginary_board(self, real_square_list):
        for square in real_square_list:
            self.square_list.append(ImaginaryTile(square.color, self.pieces))

    def create_imaginary_pieces(self, real_pieces, real_square_list):
        for piece in real_pieces:
            self.pieces.append(ImaginaryPiece(self.square_list[real_square_list.index(piece.square)], piece.name, piece.move_type))
        for square in self.square_list:
            square.piece = square.check_for_piece()


class ImaginaryInvoke:
    def __init__(self, move, board):
        # real move data
        self.move = move
        self.type = move.type
        self.real_current_sq = self.move.current_sq
        self.real_piece = self.real_current_sq.piece
        self.real_target_sq = self.move.target_sq
        # imaginary board data
        self.board = board
        self.square_list = self.board.square_list
        self.pieces = self.board.pieces
        # imaginary move data
        self.current_sq = self.square_list[self.move.board.square_list.index(self.real_current_sq)]
        self.piece = self.current_sq.piece
        self.target_sq = self.square_list[self.move.board.square_list.index(self.real_target_sq)]
        self.target_piece = self.target_sq.piece
        self.first_move = True if not self.piece.already_moved else False

    def forward(self):
        if self.type == "kill":
            self.pieces.remove(self.target_piece)
        if self.type == "check":
            self.pieces.remove(self.target_piece)
        self.current_sq.piece = None
        self.target_sq.piece = self.piece
        self.piece.square = self.target_sq
        if self.first_move:
            self.piece.already_moved = True
            self.piece.moves = self.piece.gen_moves()

    def backward(self):
        self.target_sq.piece = None
        self.current_sq.piece = self.piece
        self.piece.square = self.current_sq
        if self.type == "kill":
            self.board.pieces.append(self.target_piece)
            self.target_piece.square = self.target_sq
            self.target_sq.piece = self.target_piece
        if self.type == "check":
            self.board.pieces.append(self.target_piece)
            self.target_piece.square = self.target_sq
            self.target_sq.piece = self.target_piece
        if self.first_move:
            self.piece.already_moved = False
            self.piece.moves = self.piece.gen_moves()
