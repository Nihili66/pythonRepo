from search import Search
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
        self.allowed_moves = self.movegenerator.get_legal_moves()
        search = Search(self.board, self.player, self.allowed_moves)
        search.start_search()
        self.move = search.best_move

    def play_move(self):
        move_invoke = Invoke(self.move, self.board)
        move_invoke.forward()
        self.move = None
        self.allowed_moves = None
        self.movegenerator = None
