from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill(COLORS['red'])
        self.rect = self.image.get_rect(center = pos)

        self.direction = vector()

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector
        # direção do player
        # print(self.direction)

    def move(self,dt):
        self.rect.center += self.direction * 1
        # print ("dt ",dt)

    def update(self,dt):
        # posição do player
        # print (self.rect.center)
        self.input()
        self.move(dt)
