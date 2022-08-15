import pygame
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        # setup
        self.image = pygame.image.load('../graphics/player.png').convert()
        self.rect = self.image.get_rect(topleft=pos)
        # stats
        self.speed = 5
        self.jump_force = -16
        # interaction
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        # movement input
        if keys[pygame.K_d]:
            self.direction.x = 1  # move right
        elif keys[pygame.K_q]:
            self.direction.x = -1  # move left
        else:
            self.direction.x = 0
        # jump input
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        self.direction.y = self.jump_force
        self.collision('vertical')

    def update(self):
        self.gravity()
        self.input()
        self.move(self.speed)
