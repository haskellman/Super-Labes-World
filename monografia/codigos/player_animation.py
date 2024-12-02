def update(self,dt):
    if not self.blocked:
        self.input()
        self.move(dt)
    self.animate(dt)

def input(self):
    keys = pygame.key.get_pressed()
    input_vector = vector()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        input_vector.y -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        input_vector.y += 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        input_vector.x -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        input_vector.x += 1
    self.direction = input_vector.normalize() if input_vector else input_vector

def move(self, dt):
    self.rect.centerx += self.direction.x * self.speed *dt
    self.hitbox.centerx = self.rect.centerx
    self.collisions('horizontal')

    self.rect.centery += self.direction.y * self.speed *dt
    self.hitbox.centery = self.rect.centery
    self.collisions('vertical')
