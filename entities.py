from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)

# graphics 
        self.frame_index, self.frames = 0, frames
        self.facing_direction = 'down'

# movement 
        self.direction = vector()
        self.speed = 1000
        self.blocked = False

# sprite setup
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center = pos)
# self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)

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
      
    def change_facing_direction(self, target_pos):
        relation = vector(target_pos) - vector(self.rect.center)
        if abs(relation.y) < 30:
            self.facing_direction = 'right' if relation.x > 0 else 'left'
        else:
            self.facing_direction = 'down' if relation.y > 0 else 'up'

    def block(self):
        self.blocked = True
        self.direction = vector(0,0)

    def unblock(self):
        self.blocked = False

class Player(Entity):
    def __init__(self, pos, groups, frames):
        super().__init__(pos, frames, groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill(COLORS['red'])
        self.rect = self.image.get_rect(center = pos)

        # self.count = 0
        self.direction = vector()

    # direção do player
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
        self.direction = input_vector
        # print(self.direction)

    def move(self, dt):
        velocity = self.direction * self.speed * dt
        # self.count += 1
        # print ("dt", dt)
        self.rect.centerx += (self.direction.x * self.speed *dt) 
        # print (velocity, self.count)
        self.rect.centery += (self.direction.y * self.speed * dt)
        # print(velocity)

    def update(self,dt):
        # posição do player
        # print (self.rect.centerx, self.rect.centery, self.direction.x, self.direction.y, self.speed, dt)
        self.y_sort = self.rect.centery
        if not self.blocked:
            self.input()
            self.move(dt)
        self.animate(dt)
