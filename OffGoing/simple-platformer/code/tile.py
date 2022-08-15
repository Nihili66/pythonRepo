import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # setup
        self.image = pygame.image.load('../graphics/block.png').convert()
        self.rect = self.image.get_rect(topleft=pos)
