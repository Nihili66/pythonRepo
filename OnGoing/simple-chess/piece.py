import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, pos, groups, piece):
        super().__init__(groups)
        # setup
        self.piece = piece
        self.image = pygame.image.load('./pieces/' + piece + ".png")
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False


