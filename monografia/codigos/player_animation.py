def animate(self, dt):
    self.frame_index += ANIMATION_SPEED * dt
    self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]
    
def get_state(self):
    moving = bool(self.direction)
    if moving:
        if self.direction.x != 0:
            self.facing_direction = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.facing_direction = 'down' if self.direction.y > 0 else 'up'
    return f"{self.facing_direction}{'' if moving else '_idle'}" 

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

def update(self,dt):
    self.y_sort = self.rect.centery
    if not self.blocked:
        self.input()
        self.move(dt)
    self.animate(dt)