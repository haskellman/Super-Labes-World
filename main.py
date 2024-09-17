from settings import *
from pytmx.util_pygame import load_pygame #carrega os mapas
from os.path import join
from sprites import Sprite, AnimatedSprite, CollisionSprite, CollidableSprite
from entities import Player
from groups import AllSprites
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Amaes Game')
        self.clock = pygame.time.Clock()
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.import_assets()
        self.setup(self.tmx_maps['house'], 'house')

    def import_assets(self):
        self.tmx_maps = {
            'house': load_pygame(join('data', 'maps', 'ufes.tmx'))
            }
        self.overworld_frames = {
            'characters': all_characters_import('.', 'graphics', 'characters'),
            'water': import_folder('.', 'graphics', 'tilesets', 'water'),
            'lake': lake_importer(3, 12, '.', 'graphics', 'tilesets', 'lake'),
        }
        # print(self.overworl_frames['characters'])

    # carrega o mapa a ordem é importante pois vai sobrepor os objetos
    def setup(self,tmx_map,player_start_pos):
        # terrain 
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

		# water 
        for obj in tmx_map.get_layer_by_name('Lake'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites)
        # lake edges
        for obj in tmx_map.get_layer_by_name('Lake Edges'):
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_frames['lake'][side], self.all_sprites, WORLD_LAYERS['bg'])

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # collision
        for obj in tmx_map.get_layer_by_name('Collisions'):
            print(obj)
            CollidableSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.all_sprites, self.collision_sprites))
            # print (type((obj.width, obj.height)))
            
        # entities
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                # print(obj.x, obj.y) pos do player
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    frames = self.overworld_frames['characters']['player1'],
                    facing_direction = 'down' ,# colocar propriedade no tiled depois
                    collision_sprites = self.collision_sprites,
                )

    def run(self):
        # event loop
        while True:
            dt = self.clock.tick() / 3000 # correção de movimento para todos os pcs
            # print(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic
            self.screen.fill(COLORS['black'])
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.player)
            print (self.player.rect.center)
            # pygame.draw.rect(self.screen, self.player.rect.center, 40)


            pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()