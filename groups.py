from settings import *
from support import import_image
from entities import Entity

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.shadow = import_image('.', 'graphics', 'shadow', 'shadow')

    # camera
    def draw(self, player):
        self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
        self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)

        for sprite in self:
            if isinstance(sprite, Entity):
                self.display_surface.blit(self.shadow, sprite.rect.topleft + self.offset + vector(40, 110))
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)