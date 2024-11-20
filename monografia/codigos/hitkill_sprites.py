self.hitkill_sprites = pygame.sprite.Group() # grupo com todos os sprites de hitkill

def check_hitkill(self):
    collide = [sprite for sprite in self.hitkill_sprites if sprite.rect.colliderect(self.player.hitbox)]    
    if collide:
        self.player.kill()
