from settings import *
from pytmx.util_pygame import load_pygame #carrega os mapas
from os.path import join
from sprites import Sprite, AnimatedSprite, CollisionSprite, CollidableSprite, TransitionSprite
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
        self.transition_sprites = pygame.sprite.Group()

        # transition
        self.transition_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600
        
        self.import_assets()
        self.setup(self.tmx_maps['ufes'])

        self.dialog_tree = None

    # carrega todos os assets do jogo
    def import_assets(self):
        self.tmx_maps = import_all_maps('.', 'data', 'maps')

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
        for group in (self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites):
            group.empty()
        # terrain 
        try:
            for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])
        except:
            pass

		# water 
        try:
            for obj in tmx_map.get_layer_by_name('Lake'):
                for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                    for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                        AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, GAME_LAYERS['water'])
        except:
            pass

        # lake edges
        try:
            if tmx_map.get_layer_by_name('Lake Edges'):
                for obj in tmx_map.get_layer_by_name('Lake Edges'):
                    side = obj.properties['side']
                    AnimatedSprite((obj.x, obj.y), self.overworld_frames['lake'][side], self.all_sprites, GAME_LAYERS['bg'])
        except:
            pass

        # objects
        try:
            for obj in tmx_map.get_layer_by_name('Objects'):
                if obj.name == 'passarela_ufes':
                    Sprite((obj.x, obj.y), obj.image, self.all_sprites, GAME_LAYERS['top'])
                else:
                    print(obj)
                    CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        except:
            pass

        # collision
        try:
            for obj in tmx_map.get_layer_by_name('Collisions'):
                print(obj)
                CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.all_sprites, self.collision_sprites))
                # print (type((obj.width, obj.height)))
        except: 
            pass

        # transitions
        try:
            for obj in tmx_map.get_layer_by_name('Transitions'):
                # print(obj.x, obj.y, obj.properties['dest'], obj.properties['src'])
                TransitionSprite((obj.x, obj.y), obj.properties['dest'], obj.properties['src'], self.transition_sprites, (obj.width, obj.height))
        except:
            pass

        # entities
        try:
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
        except:
            pass

    # verifica o input do jogador
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
            self.dialog_tree = Dialog(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

    def end_dialog(self,character):
        self.dialog_tree = None
        self.player.unblock()

    def check_transitions(self):
        transition_area = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if transition_area:
            self.player.block()
            self.transition_dest = transition_area[0].dest
            self.tint_mode = 'tint'

    def tint(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt    
            if self.tint_progress >= 255: 
            # falta pegar o nome do mapa
                self.setup(self.tmx_maps[self.transition_dest])
                self.tint_mode = 'untint'
                self.transition_target = None

        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.screen.blit(self.tint_surf, (0,0))

    def run(self):
        # event loop
        while True:
            self.screen.fill(COLORS['black'])
            dt = self.clock.tick() / 1000 # correção de movimento para todos os pcs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic
            self.input()
            self.check_transitions()
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.player)

            # overlays
            if self.dialog_tree: self.dialog_tree.update()
            
            self.tint(dt)
            pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()