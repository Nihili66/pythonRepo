class Move:
    def __init__(self, current_sq, target_sq, board):
        self.board = board
        self.current_sq = current_sq
        self.target_sq = target_sq
        self.type = self.get_move_type()
        self.check_squares = self.get_check_squares()

    def get_move_type(self):
        if not self.target_sq.piece:
            return "normal"
        elif self.target_sq.piece.color != self.current_sq.piece.color:
            if self.target_sq.piece.type == "king":
                return "check"
            else:
                return "kill"

    def get_check_squares(self):
        if self.type == "check":
            check_squares = []
            if self.current_sq.piece.type == "rook":
                sq_difference = - self.board.square_list.index(self.target_sq) + self.board.square_list.index(self.current_sq)
                if 7 >= sq_difference >= -7:
                    for i in range(abs(sq_difference) + 1):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i])
                elif sq_difference % 8 == 0:
                    for i in range(abs(sq_difference) // 8):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i * 8])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i * 8])
            elif self.current_sq.piece.type == "bishop":
                sq_difference = - self.board.square_list.index(self.target_sq) + self.board.square_list.index(self.current_sq)
                if sq_difference % 7 == 0:
                    for i in range(abs(sq_difference) // 7):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i * 7])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i * 7])
                elif sq_difference % 9 == 0:
                    for i in range(abs(sq_difference) // 9):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i * 9])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i * 9])
            elif self.current_sq.piece.type == "queen":
                sq_difference = - self.board.square_list.index(self.target_sq) + self.board.square_list.index(self.current_sq)
                if 7 >= sq_difference >= -7:
                    for i in range(abs(sq_difference) + 1):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i])
                elif sq_difference % 8 == 0:
                    for i in range(abs(sq_difference) // 8):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i * 8])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i * 8])
                elif sq_difference % 7 == 0:
                    for i in range(abs(sq_difference) // 7):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i * 7])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i * 7])
                elif sq_difference % 9 == 0:
                    for i in range(abs(sq_difference) // 9):
                        if sq_difference > 0:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) + i * 9])
                        else:
                            check_squares.append(self.board.square_list[self.board.square_list.index(self.target_sq) - i * 9])
            elif self.current_sq.piece.move_type == "normal":
                check_squares.append(self.current_sq)
            return check_squares



