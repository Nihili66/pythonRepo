import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # movement
        self.direction = pygame.math.Vector2()
        self.gravity_force = 8

    def gravity(self):
        # if self.direction.y == 0:
        self.direction.y += self.gravity_force
        self.rect.y += self.direction.y
        self.collision('vertical')

    def move(self, speed):
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')

    def collision(self, direction):
        # normal collisions
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:  # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # moving left
                        self.rect.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0
                    if self.direction.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
