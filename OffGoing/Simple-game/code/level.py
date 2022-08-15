import pygame
import time
from settings import *
from tile import Tile
from player import Player
from debug import debug
from enemy import Enemy
from weapon import Weapon

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite groups setup
        self.visible_sprites = YsortCamera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    tree_image = pygame.image.load('../graphics/tile/tree.png').convert_alpha()
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], tree_image)
                if col == 'r':
                    rock_image = pygame.image.load('../graphics/tile/rock.png').convert_alpha()
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], rock_image)
                if col == 'c':
                    coin_image = pygame.image.load('../graphics/collectible/goldcoin1.png').convert_alpha()
                    Tile((x, y), [self.visible_sprites, self.collectible_sprites], coin_image)
                if col == 'e':
                    enemy_image = pygame.image.load('../graphics/enemy/enemy.png').convert_alpha()
                    self.enemy = Enemy((x, y), [self.visible_sprites, self.attackable_sprites], enemy_image)
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.collectible_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(3, self.player, [self.visible_sprites], self.attackable_sprites)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.enemy.hp)

class YsortCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.center_width = self.display_surface.get_size()[0] // 2
        self.center_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = self.center_width - player.rect.centerx
        self.offset.y = self.center_height - player.rect.centery
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
