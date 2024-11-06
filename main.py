from settings import *
from pytmx.util_pygame import load_pygame #carrega os mapas
from os.path import join
from sprites import Sprite, AnimatedSprite, CollisionSprite, CollidableSprite, TransitionSprite, DialogSprite, InteractiveSprite
from entities import Player, Character, Entity
from inventory import Inventory
from computer import Computer
from battle import Battle
from choose_dialog import ChooseDialog
from item import Item
from link import Link
from groups import AllSprites
from support import *
from game_data import *
from dialog import Dialog
from timer import Timer
from time import sleep
class Game:
    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Amaes Game')
        self.clock = pygame.time.Clock()
        self.buff_timer = Timer(15000, autostart = True)
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites   = pygame.sprite.Group()
        self.character_sprites   = pygame.sprite.Group()
        self.transition_sprites  = pygame.sprite.Group()
        self.dialogs_sprites     = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # transition
        self.transition_area = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = 1
        self.tint_speed = 600

        self.import_assets()

        self.current_map = 'house'
        self.audios = audio_importer('.', 'audios')
        self.sounds = audio_importer('.', 'sounds')

        # mapa iniciais
        self.setup(self.tmx_maps['house'], 'house', 'house') #house
        # self.setup(self.tmx_maps['ponto_onibus'], 'ponto_onibus', 'house') #ponto_onibus
        # self.setup(self.tmx_maps['ufes'], 'ufes', 'ponto_onibus') #ufes
        # self.setup(self.tmx_maps['ct7'], 'ct7', 'ufes') #ct7
        # self.setup(self.tmx_maps['sala_vitor'], 'sala_vitor', 'ct7') #sala_vitor
        # self.setup(self.tmx_maps['sala_monalessa'], 'sala_monalessa', 'ct7') #sala_monalessa
        # self.setup(self.tmx_maps['sala_patricia'], 'sala_patricia', 'ct7') #sala_patricia
        # self.setup(self.tmx_maps['ct9'], 'ct9', 'ufes') #ct9
        # self.setup(self.tmx_maps['labgrad'], 'labgrad', 'ct9') labrad
    
        

        # Computer
        self.computer_links = []
        self.create_computer()

        # Inventory
        self.player_items = []
        self.create_inventory()

        # overlays
        self.dialog_open = None
        self.inventory = Inventory(self.player_items , self.fonts, self.interface_frames, self.player, self.sounds, self.item_used)
        self.inventory_open = False
        self.computer = Computer(self.computer_links,self.fonts, self.interface_frames, self.sounds)
        self.computer_open = False
        self.battle_open = False
        self.choose_dialog_open = False


        # items iniciais
        # self.add_item(Item('0'))
        # self.add_item(Item('1'))
        # self.add_item(Item('2'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))
        self.add_item(Item('4'))

# ------------------------------------------------------------------------------------------------------------------------------------
    #  Computer functions
    def add_link(self, item):
        self.computer_links.append(item)

    def create_computer(self):
        for i in COMPUTER_DATA:
            self.add_link(Link(i))
    
    def clean_computer(self):
        self.computer_links = []

    def create_computer_by_result(self, list, character):
        for index, item in enumerate(list):
            if item == 0:
                self.add_link(Link(character.questions[index]['link']))
    
    # Inventory functions
    def create_inventory(self):
        inventory_size = 30
        for _ in range(inventory_size):
            self.player_items.append({})

    def add_item(self, item):
        for index, item_ in enumerate(self.player_items):
            if (item_ == {}):
                self.player_items[index] = item
                break

    def check_item(self, item):
        for index, item_ in enumerate(self.player_items):
            if (item_ != {} and item_.name == item.name):
                return True
        return False
 
            

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
            'bold': pygame.font.Font(join('.', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
            'regular': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
            'regular_mid': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 22),
            'regular_big': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 34),
        }
        self.interface_frames = {
            'interface': import_folder_dict('.', 'graphics', 'interface'),
            'items': import_folder_dict('.', 'graphics', 'items'),
            'interactive_objects': import_folder_dict('.', 'graphics', 'interactive_objects'),
        }

    # carrega o mapa a ordem é importante pois vai sobrepor os objetos
    def setup(self,tmx_map, dest_map, src_map):
        self.current_map = dest_map
        # clean sprites
        for group in (self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites, self.dialogs_sprites, self.interaction_sprites):
            group.empty()
        # terrain 
        # map theme
        self.audios[src_map].stop()
        self.audios[dest_map].play(-1)   

        # Terreno
        try:
            for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])
        except ValueError as ve:
           pass
            # manter os items do jogador aqui

        # Coisas acima do terreno sem colisão
        try:
            for x, y, surf in tmx_map.get_layer_by_name('Terrain Top').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])
        except ValueError as ve:
           pass

        # Objetos em cima do terreno
        try:
            for obj in tmx_map.get_layer_by_name('Terrain Objects'):
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, GAME_LAYERS['bg'])
        except ValueError as ve:
            pass

		# agua
        try:
            for obj in tmx_map.get_layer_by_name('Lake'):
                for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                    for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                        AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, GAME_LAYERS['water'])
        except ValueError as ve:
            pass

        # bordas do lago
        try:
            if tmx_map.get_layer_by_name('Lake Edges'):
                for obj in tmx_map.get_layer_by_name('Lake Edges'):
                    side = obj.properties['side']
                    AnimatedSprite((obj.x, obj.y), self.overworld_frames['lake'][side], self.all_sprites, GAME_LAYERS['bg'])
        except ValueError as ve:
            pass

        # objetos
        try:
            for obj in tmx_map.get_layer_by_name('Objects'):
                CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        except ValueError as ve:
            pass

        # objetos interativos 
        try:
            for obj in tmx_map.get_layer_by_name('Interactive Objects'):
                InteractiveSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.interaction_sprites, self.collision_sprites), obj.properties['item_id'])
        except ValueError as ve:
            pass

        # Colisões invisíveis
        try:
            for obj in tmx_map.get_layer_by_name('Collisions'):
                CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.collision_sprites))
        except ValueError as ve:
           pass

        # dialogs
        
        if (not tmx_map in VISITED_MAPS):
            VISITED_MAPS.append(tmx_map)
            try:
                for obj in tmx_map.get_layer_by_name('Dialogs'):
                    DialogSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.dialogs_sprites), obj.properties['message'])
                    # print (type((obj.width, obj.height)))
            except ValueError as ve:
               pass

        # transitions
        try:
            for obj in tmx_map.get_layer_by_name('Transitions'):
                # print(obj.x, obj.y, obj.properties['dest'], obj.properties['src'])
                TransitionSprite((obj.x, obj.y), obj.properties['dest'], obj.properties['src'], self.transition_sprites, (obj.width, obj.height))
        except ValueError as ve:
           pass

        # entities
        try:
            for obj in tmx_map.get_layer_by_name('Entities'):
                if obj.name == 'Player':
                    # print(obj.x, obj.y) # pos do player
                    if obj.properties['pos'] == src_map:
                        self.player = Player(
                            pos = (obj.x, obj.y),
                            groups = self.all_sprites,
                            frames = self.overworld_frames['characters']['player1'],
                            facing_direction = obj.properties['direction'],
                            collision_sprites = self.collision_sprites,
                            character_data = CHARACTERS_DATA[obj.properties['character_id']],
                        )
                else:
                    Character(
                        pos = (obj.x, obj.y), 
                        groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
                        frames = self.overworld_frames['characters'][obj.properties['graphic']], 
                        facing_direction = obj.properties['direction'],
                        collision_sprites = self.collision_sprites,
                        character_data = CHARACTERS_DATA[obj.properties['character_id']],
                    )
        except ValueError as ve:
           pass

    # verifica a entrada do jogador
    def input(self):
        if not self.dialog_open and not self.choose_dialog_open and not self.battle_open:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE] and not self.dialog_open:
                # interações com personagens
                for character in self.character_sprites:
                    if check_connections(100, self.player, character):
                        character.change_facing_direction(self.player.rect.center)
                        self.create_dialog(character)
                # interações com objetos
                for sprite in self.interaction_sprites:
                    if check_interaction(150, self.player, sprite):
                        if sprite.item_id == 'computer':
                            self.computer_open = not self.computer_open
                            self.player.blocked = not self.player.blocked
                            break
                            # emitir som
                        if sprite.item_id == 'coffe':
                            self.add_item(Item('4'))
                            self.sounds['get_item'].play()
                            sprite.kill()
                            break
                        if sprite.item_id == 'abajour1':
                            sprite.item_id = 'abajour2'
                            sprite.image = self.interface_frames['interactive_objects']['abajour2']
                            break
                        if sprite.item_id == 'abajour2':
                            sprite.item_id = 'abajour1'
                            sprite.image = self.interface_frames['interactive_objects']['abajour1']
                            break
                        if sprite.item_id == 'dragon':
                            self.create_dialog(self.player, "acho melhor eu não acorda-lo", False)
                        if sprite.item_id == 'placa_prograd':
                            self.create_dialog(self.player, "A placa diz: 'Prograd - Pró-Reitoria de Graduação'...\n\n o labes deve estar mais a frente", False)
                        if sprite.item_id == 'placa_ic1':
                            self.create_dialog(self.player, "A placa diz: 'IC1 - Centro de Ciências Exatas'...\n\no labes deve estar mais a frente", False)
                        if sprite.item_id == 'placa_ic2':
                            self.create_dialog(self.player, "A placa diz: 'IC2 - CCHN | Centro de Ciências Humanas e Naturais'...\n\no labes deve estar mais a frente", False)
                        if sprite.item_id == 'placa_ic3':
                            self.create_dialog(self.player, "A placa diz: 'IC3 - CCHN | Centro de Ciências Humanas e Naturais'...\n\no labes deve estar mais a frente", False)
                        if sprite.item_id == 'placa_ic4':
                            self.create_dialog(self.player, "A placa diz: 'IC4 - CE | Centro de Educação'...\n\nsinto que estou próximo", False)
                        if sprite.item_id == 'placa_ct3':
                            self.create_dialog(self.player, "A placa diz: 'CT3 - Centro Tecnológico'...\n\nessas numerações de ct não fazem sentido algum!! ", False)
                        if sprite.item_id == 'placa_ct7':
                            self.create_dialog(self.player, "A placa diz: 'CT7 - Centro Tecnológico'...\n\nFinalmente cheguei ", False)
                        if sprite.item_id == 'placa_ct9':
                            self.create_dialog(self.player, "A placa diz: 'CT9 - Centro Tecnológico'...\n\ntalvez eu deva estudar aqui antes do meu teste", False)
                        if sprite.item_id == 'placa_ct10':
                            self.create_dialog(self.player, "A placa diz: 'CT10 - Centro Tecnológico'...\n\nopa o ct9 é logo acima", False)
                        if sprite.item_id == 'placa_ct12':
                            self.create_dialog(self.player, "A placa diz: 'CT12 - Centro Tecnológico'...\n\no ct7 deve ser logo acima ", False)
                        if sprite.item_id == 'placa_vire_esquerda':
                            self.create_dialog(self.player, "A placa diz: CT7 e CT9 a esquerda'...\n\n...que coisa! parece que essas placas sabem pra onde eu quero ir ", False)
                        if sprite.item_id == 'placa_cantina':
                            self.create_dialog(self.player, "A placa diz: 'Cantina'...\n\n...hummm cheirinho de gordura ", False)
                        if sprite.item_id == 'placa_ru':
                            self.create_dialog(self.player, "A placa diz: Restaurante Universitário'...\n\n...poh bateu a fome... mas está fechado ", False)
                        if sprite.item_id == 'placa_bc':
                            self.create_dialog(self.player, "A placa diz: Biblioteca Central'...\n\n...eu até que estudaria... mas está fechado ", False)
                        if sprite.item_id == 'placa_lake':
                            self.create_dialog(self.player, "A placa diz: Lagoa da Ufes Reza a lenda que sua água é radioativa'...\n\n...'-' ", False)
            # inventario
            if keys[pygame.K_i]:
                self.inventory_open = not self.inventory_open
                self.player.blocked = not self.player.blocked
                # emitir som
            # fechar sobreposições
            if keys[pygame.K_ESCAPE]:
                self.inventory_open = False
                self.computer_open = False
                self.player.blocked = False

    def item_used(self):
        self.player.speed_boost(1.5)
        self.buff_timer.activate()


    def create_dialog(self, character, message = None, collision_message = True):
        if not self.dialog_open:
            self.sounds['notice'].play()
            self.player.block()
            self.dialog_open = Dialog(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog, message, collision_message)

    # Callback functions
    def end_dialog(self,character):
        self.dialog_open = None
        # batalha
        if check_battle(character) and not self.battle_open and character.character_data['visited'] == False:
            self.player.block()
            # dialogo de escolha
            self.player.block()
            self.choose_dialog = ChooseDialog(character, self.interface_frames, self.fonts, self.end_choose_dialog)
            self.choose_dialog_open = True
        # item
        elif character.character_data['name'] != 'player' and character.character_data['visited'] != False and character.character_data['visited'] == True and character.character_data['item'] != None:
            self.sounds['get_item'].play()
            self.add_item(Item(character.character_data['item']))
            character.character_data['item'] = None
        if not self.choose_dialog_open:
            # self.dialog_open = None
            self.player.unblock()
            character.character_data['visited'] = True

    def end_choose_dialog(self, answer, character):
        if answer:
            self.audios[self.current_map].stop()
            self.audios['battle'].play(-1)
            self.choose_dialog_open = False
            self.player.block()
            self.tint_mode = 'battle_mode'
            sleep(2)
            self.battle = Battle(self.player, character, self.interface_frames, self.fonts, self.end_battle, self.sounds)
            self.dialog_open = None
            self.battle_open = True
        else:
            self.create_dialog(character, "hahaha, veio de tão longe para arregar?", False)
            # self.dialog_open = None
            self.choose_dialog_open = False
            self.player.unblock()
        self.dialog_open = None

    def end_battle(self, character, test):
        result = sum(test)
        self.tint_mode = 'battle_mode'
        sleep(2)
        self.audios['battle'].stop()
        self.audios[self.current_map].play(-1)
        self.battle_open = False
        text = 'voce acertou ' + str(result) + ' das ' + str(len(test))  + ' perguntas'
        if (result >= 7):
            self.sounds['correct_answer'].play()
            character.character_data['visited'] = True
            self.create_dialog(character, text + ' tome... pode ficar com a chave\ncheque no computador as questões que voce errou', False)
        else:
            self.sounds['wrong_answer'].play()
            self.create_dialog(character, text, False)
        self.clean_computer()
        self.create_computer_by_result(test, character)
        self.computer = Computer(self.computer_links,self.fonts, self.interface_frames, self.sounds)

    # verifica se o player colidiu com uma transição
    # para entrar na sala da monalessa é necessário ter a chave 0 do vitor
    # para entrar na sala da patricia é necessário ter a chave 1 da monalessa
    # para vencer o jogo é necessário ter as 3 chaves
    def check_transitions(self):
        transition_rect = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]    
        if transition_rect:
            # restrição sala monalessa
            if transition_rect[0].dest == 'sala_monalessa' and not self.check_item(Item('0')):
                self.sounds['51 - MMX - Can\'t Exit'].play()
            # restrição sala patricia
            elif transition_rect[0].dest == 'sala_patricia' and not self.check_item(Item('1')):
                self.sounds['51 - MMX - Can\'t Exit'].play()
            # restrição sala final
            elif transition_rect[0].dest == 'end' and (not self.check_item(Item('0')) or not self.check_item(Item('1')) or not self.check_item(Item('2'))):
                self.sounds['51 - MMX - Can\'t Exit'].play()
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    print('implementar')
            else:       
                self.player.block()
                self.transition_area = transition_rect
                self.tint_mode = 'tint'

    # verifica se o player colidiu com uma caixa de dialogo
    def check_dialog(self):
        for sprite in self.dialogs_sprites:
            if sprite.hitbox.colliderect(self.player.hitbox):
                self.create_dialog(self.player, sprite.message)
                sprite.kill()

    # efeitos de status do player
    def player_effects(self):
        # timer
        if not self.buff_timer.active:
            self.player.speed = 350

    # efeito de transição
    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt    
            if self.tint_progress >= 255:
                dest_map = self.transition_area[0].dest
                src_map = self.transition_area[0].src
                self.setup(self.tmx_maps[dest_map], dest_map, src_map)
                self.tint_mode = 'untint'
                self.transition_area = None
        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.screen.blit(self.tint_surf, (0,0))

    # efeito de transição
    def tint_battle(self, dt):
        if self.tint_mode == 'end_battle':
            self.tint_progress -= self.tint_speed * dt * 0.3
        if self.tint_mode == 'battle_mode':
            self.tint_progress += self.tint_speed * dt * 0.3
            if self.tint_progress >= 255:
                self.tint_mode = 'end_battle'
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
            self.check_dialog()
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.player)

            # overlays
            if self.dialog_open: self.dialog_open.update()
            if self.inventory_open: self.inventory.update(dt)
            if self.computer_open: self.computer.update(dt)
            if self.battle_open: self.battle.update(dt)
            if self.choose_dialog_open: self.choose_dialog.update()

            # print('Dialog', self.dialog_open)
            # print('Inventory', self.inventory_open)
            # print('Computer', self.computer_open)
            # print('Battle', self.battle_open)
            # print('Choose Dialog', self.choose_dialog_open)

            # tint
            self.tint_screen(dt)
            self.tint_battle(dt)
            pygame.display.update()

            # player buffs
            self.player_effects()
            self.buff_timer.update()

if __name__ == '__main__':
	game = Game()
	game.run()