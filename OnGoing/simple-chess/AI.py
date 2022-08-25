from movegenerator import MoveGenerator

class AiMovement:
    def __init__(self):
        self.movegenerator = None
        self.current_sq = None
        self.piece = None
        self.target_sq = None
        self.allowed_moves = []
