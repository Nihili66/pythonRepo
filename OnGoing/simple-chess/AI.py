from search import Search
from invokemove import Invoke
from movegenerator import MoveGenerator

class AiMovement:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.movegenerator = MoveGenerator(self.board)
        self.legal_moves = None
        self.move = None

    def pick_move(self):
        self.legal_moves = self.movegenerator.get_legal_moves()
        search = Search(self.board, self.player, self.legal_moves)
        self.move = search.start_search(2)

    def play_move(self):
        move_invoke = Invoke(self.move, self.board)
        move_invoke.forward()
