from evaluation import Evaluate
from imagination import ImaginaryBoard, ImaginaryInvoke
from movegenerator import MoveGenerator

class Search:
    def __init__(self, board, ai_player, ai_moves):
        # real board
        self.real_board = board
        # imaginary board
        self.board = self.board = ImaginaryBoard(self.real_board)
        self.players = self.board.players
        # player
        self.ai = ai_player
        self.player = self.get_imaginary_players("player")
        self.enemy = self.get_imaginary_players("enemy")
        # player moves
        self.ai_moves = ai_moves
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
        best_move_this_turn = None
        best_eval_this_turn = None
        for move in self.ai_moves:
            # invoke the player's move
            move_invoke = ImaginaryInvoke(move, self.board)
            move_invoke.forward()
            # iterate through the enemy's moves
            best_enemy_eval = self.search(depth)
            if not best_move_this_turn:
                best_move_this_turn = move
                best_eval_this_turn = - best_enemy_eval
            else:
                if -best_enemy_eval > best_eval_this_turn:
                    best_move_this_turn = move
                    best_eval_this_turn = -best_enemy_eval
            # reset the player's move
            move_invoke.backward()
        self.best_move = best_move_this_turn
        return self.best_move

    def search(self, depth):
        if depth == 0:
            evaluator = Evaluate(self.board)
            return evaluator.evaluate_board()

        # generate the enemy's moves
        generator = MoveGenerator(self.board)
        moves = generator.get_legal_moves()
        best_eval = None

        for move in moves:
            move_invoke = ImaginaryInvoke(move, self.board)
            move_invoke.forward()
            evaluation = - self.search(depth - 1)
            best_eval = evaluation if not best_eval else max(best_eval, evaluation)
            move_invoke.backward()
        return best_eval
