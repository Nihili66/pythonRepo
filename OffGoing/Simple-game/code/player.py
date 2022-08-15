import pygame
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, collectible_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        # setup
        self.status = 'down'
        self.animation(self.status)
        self.rect = self.image.get_rect(topleft=pos)
        # movement
        self.attack_now = 0
        # stats
        self.speed = 5
        self.score = 0
        # interactions
        self.obstacle_sprites = obstacle_sprites
        self.collectible_sprites = collectible_sprites
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

    def input(self):
        if self.attack_now == 0:
            keys = pygame.key.get_pressed()
            # movement input
            if keys[pygame.K_z]:
                self.direction.y = -1 # move up
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1 # move down
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_d]:
                self.direction.x = 1 # move right
                self.status = 'right'
            elif keys[pygame.K_q]:
                self.direction.x = -1 # move left
                self.status = 'left'
            else:
                self.direction.x = 0
            # attack input
            if keys[pygame.K_c]:
                self.attack_now = 1
                self.create_attack()
        else:
            self.attack_now = 0
            self.destroy_attack()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def animation(self, direction):
        if direction == 'down':
            self.image = pygame.image.load('../graphics/player/down.png')
        elif direction == 'up':
            self.image = pygame.image.load('../graphics/player/up.png')
        elif direction == 'left':
            self.image = pygame.image.load('../graphics/player/left.png')
        elif direction == 'right':
            self.image = pygame.image.load('../graphics/player/right.png')

    def update(self):
        self.input()
        self.animation(self.status)
        self.move(self.speed)
