from settings import *
from pytmx.util_pygame import load_pygame #carrega os mapas
from os.path import join
from sprites import Sprite, AnimatedSprite, CollisionSprite, CollidableSprite
from entities import Player, Character
from groups import AllSprites
from support import *
from game_data import *
from dialog import Dialog

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Amaes Game')
        self.clock = pygame.time.Clock()
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        
        self.import_assets()
        self.setup(self.tmx_maps['house'])

        self.dialog_tree = None

    def import_assets(self):
        self.tmx_maps = {
            'house': load_pygame(join('data', 'maps', 'ufes.tmx'))
            }
        self.overworld_frames = {
            'characters': all_characters_import('.', 'graphics', 'characters'),
            'water': import_folder('.', 'graphics', 'tilesets', 'water'),
            'lake': lake_importer(3, 12, '.', 'graphics', 'tilesets', 'lake'),
        }
        self.fonts = {
            'dialog': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
        }

    # carrega o mapa a ordem é importante pois vai sobrepor os objetos
    def setup(self,tmx_map):
        # terrain 
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])

		# water 
        for obj in tmx_map.get_layer_by_name('Lake'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, GAME_LAYERS['water'])
        # lake edges
        for obj in tmx_map.get_layer_by_name('Lake Edges'):
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_frames['lake'][side], self.all_sprites, GAME_LAYERS['bg'])

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'passarela_ufes':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, GAME_LAYERS['top'])
            else:
                print(obj)
                CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # collision
        for obj in tmx_map.get_layer_by_name('Collisions'):
            print(obj)
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.all_sprites, self.collision_sprites))
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
                    collision_sprites = self.collision_sprites
                )
            else:
                Character(
                    pos = (obj.x, obj.y), 
                    groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
                    frames = self.overworld_frames['characters'][obj.properties['graphic']], 
                    facing_direction = obj.properties['direction'],
                    collision_sprites = self.collision_sprites,
                    character_data = CHARACTER_DATA[obj.properties['character_id']],
                )


                print(self.collision_sprites)

    def input(self):
        if not self.dialog_tree:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE] and not self.dialog_tree:
                for character in self.character_sprites:
                    if check_connections(100, self.player, character):
                        self.player.block()
                        character.change_facing_direction(self.player.rect.center)
                        self.create_dialog(character)

    def create_dialog(self, character):
        if not self.dialog_tree:
            print('só')
            self.dialog_tree = Dialog(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

    def end_dialog(self,character):
        self.dialog_tree = None
        self.player.unblock()

    def run(self):
        # event loop
        while True:
            self.screen.fill(COLORS['black'])
            dt = self.clock.tick() / 1000 # correção de movimento para todos os pcs
            # print(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic
            self.input()
            # pygame.draw.rect(self.screen, (255,0,0), self.player.hitbox,3)
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.player)
            # print (self.player.rect.center)
            # pygame.draw.rect(self.screen, self.player.rect.center, 40)

            # overlays
            if self.dialog_tree: self.dialog_tree.update()


            pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()