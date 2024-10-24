import pygame
from settings import *
# overworld sprites
class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = GAME_LAYERS['main']):
		super().__init__(groups)
		self.image = surf 
		self.rect = self.image.get_frect(topleft = pos) #frect float rect numeros mais precisos
		self.y_sort = self.rect.centery
		self.hitbox = self.rect.copy()
		self.z = z

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = GAME_LAYERS['main']):
		self.frame_index, self.frames = 0, frames
		super().__init__(pos, frames[self.frame_index], groups)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)

class CollisionSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy()

class CollidableSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)

class TransitionSprite(Sprite):
	def __init__(self, pos, dest, src, groups, size):
		super().__init__(pos, pygame.Surface((size)), groups)
		self.src = src
		self.dest = dest

class DialogSprite(Sprite):
	def __init__(self, pos, surf, groups, message):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy()
		self.message = message