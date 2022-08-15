import pygame
from settings import TILESIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color):
        super().__init__(groups)
        # setup
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
