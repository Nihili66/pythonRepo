import random
from invokemove import Invoke
from movegenerator import MoveGenerator

class AiMovement:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.movegenerator = None
        self.allowed_moves = None
        self.move = None

    def pick_move(self):
        self.movegenerator = MoveGenerator(self.board, self.player)
        self.movegenerator.generate_allowed_moves()
        self.allowed_moves = self.movegenerator.legal_moves
        for move in self.allowed_moves:
            if move.type == "kill":
                self.move = move
        if not self.move:
            self.move = random.choice(self.allowed_moves)

    def play_move(self):
        move_invoke = Invoke(self.move, self.board)
        move_invoke.forward()
        self.move = None
