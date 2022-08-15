# chess piece collision detection
 def check_collision(sprite, group):
     for sprite in group:
         if sprite.rect.colliderect(sprite.rect):
             return True
     return False