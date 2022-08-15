import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, ap, player, groups, attackable_sprites):
        super().__init__(groups)
        # interactions
        self.attackable_sprites = attackable_sprites
        self.player = player
        direction = self.player.status
        # setup
        full_path = f'../graphics/weapon/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
        # stats
        self.power = ap
        # attack
        for sprite in self.attackable_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.hp -= self.power
