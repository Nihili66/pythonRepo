from search import Search
from invokemove import Invoke

class AiMovement:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.move = None

    def pick_move(self):
        search = Search(self.board, self.player)
        self.move = search.start_search(5)

    def play_move(self):
        move_invoke = Invoke(self.move, self.board)
        move_invoke.forward()
