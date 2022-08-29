from evaluation import Evaluate
from imagination import ImaginaryBoard, ImaginaryInvoke
from movegenerator import MoveGenerator

class Search:
    def __init__(self, board, ai_player, ai_moves):
        # real board
        self.real_board = board
        self.players = self.real_board.players
        # player
        self.board = self.board = ImaginaryBoard(self.real_board)
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

    def search(self):
        best_move_this_turn = None
        best_eval_this_turn = None
        for move in self.ai_moves:
            # invoke the player's move
            move_invoke = ImaginaryInvoke(move, self.board)
            move_invoke.forward()
            # generate the enemy's moves
            enemy_generator = MoveGenerator(self.board, self.enemy)
            enemy_moves = enemy_generator.get_legal_moves()
            # iterate through the enemy's moves
            best_enemy_eval = None
            for enemy_move in enemy_moves:
                # invoke the enemy's move
                enemy_move_invoke = ImaginaryInvoke(enemy_move, self.board)
                enemy_move_invoke.forward()
                # evaluate the enemy's move
                enemy_evaluator = Evaluate(self.board, self.enemy)
                enemy_eval = enemy_evaluator.evaluate_board()
                # the first iteration
                if not best_enemy_eval:
                    best_enemy_eval = enemy_eval
                else:
                    if enemy_eval > best_enemy_eval:
                        best_enemy_eval = enemy_eval
                # reset the enemy's move
                enemy_move_invoke.backward()
            # the first iteration
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

    def start_search(self):
        self.search()
        return self.best_move
