import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, graphic):
        super().__init__(groups)
        self.image = graphic
        self.rect = self.image.get_rect(topleft=pos)
