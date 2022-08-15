import pygame
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, groups, graphic):
        super().__init__(groups)
        # setup
        self.image = graphic
        self.rect = self.image.get_rect(topleft=pos)
        # stats
        self.speed = 4
        self.hp = 100

    def death(self):
        if self.hp <= 0:
            self.kill()
        else:
            pass

    def update(self):
        self.death()
