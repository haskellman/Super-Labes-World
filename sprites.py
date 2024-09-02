import pygame
# overworld sprites
class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf 
		self.rect = self.image.get_frect(topleft = pos) #frect float rect numeros mais precisos
		self.y_sort = self.rect.centery
		self.hitbox = self.rect.copy()
