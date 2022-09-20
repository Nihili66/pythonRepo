from evaluation import Evaluate
from invokemove import ImaginaryInvoke
from movegenerator import MoveGenerator

class Search:
    def __init__(self, board, ai_player):
        # board
        self.board = board
        self.players = self.board.players
        self.depth = None
        # player
        self.ai = ai_player
        self.player = self.get_imaginary_players("player")
        self.enemy = self.get_imaginary_players("enemy")
        # player moves
        self.alpha = -1000000
        self.beta = 1000000
        self.best_move = None

    def get_imaginary_players(self, ptype):
        for player in self.players:
            if ptype == "player":
                if player.color == self.ai.color:
                    return player
            elif ptype == "enemy":
                if player.color != self.ai.color:
                    return player

    def start_search(self, depth):
        self.depth = depth
        self.best_move = self.search(depth, self.alpha, self.beta)
        return self.best_move

    def search(self, depth, alpha, beta):
        if depth == 0:
            evaluator = Evaluate(self.board)
            return evaluator.evaluate_board()
        # generate the moves
        generator = MoveGenerator(self.board)
        moves = generator.get_legal_moves()
        best_eval = None
        best_move = None
        for move in moves:
            move_invoke = ImaginaryInvoke(move, self.board)
            move_invoke.forward()
            evaluation = - self.search(depth - 1, -beta, -alpha)
            if depth == self.depth:
                if not best_eval:
                    best_move = move
                    best_eval = evaluation
                else:
                    if evaluation > best_eval:
                        best_move = move
                        best_eval = evaluation

                move_invoke.backward()
            else:
                move_invoke.backward()
                if evaluation >= beta:
                    return beta
                alpha = max(alpha, evaluation)
        if depth == self.depth:
            return best_move
        else:
            return alpha
