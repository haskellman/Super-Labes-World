from settings import *
from os.path import join
from home import Home
from credits import Credits
from game_controls import GameControls
from sprites import Sprite, AnimatedSprite, CollisionSprite, CollidableSprite, TransitionSprite, CollidableDialogSprite, InteractiveSprite
from entities import Player, Character
from inventory import Inventory
from computer import Computer
from battle import Battle
from choose_dialog import ChooseDialog
from item import Item
from link import Link
from all_sprites import AllSprites
from support import *
from game_data import *
from dialog import Dialog
from timer import Timer
from time import sleep
class Game:
    def __init__(self): 
        # inicialização
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.buff_timer = Timer(15000, autostart = True) # 15 segundos
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites   = pygame.sprite.Group()
        self.character_sprites   = pygame.sprite.Group()
        self.transition_sprites  = pygame.sprite.Group()
        self.collidable_dialogs_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # transition
        self.transition_area = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = 1
        self.tint_speed = 600

        # importação de todos os assets
        self.import_assets()

        # audios e efeitos sonoros
        self.current_map = 'house'
        self.audios = audio_importer('.', 'audios')
        self.sounds = audio_importer('.', 'sounds')

        # mapas iniciais
        self.setup(self.tmx_maps['house'], 'house', 'house') #house
        # self.setup(self.tmx_maps['ponto_onibus'], 'ponto_onibus', 'house') #ponto_onibus
        # self.setup(self.tmx_maps['ufes'], 'ufes', 'ponto_onibus') #ufes
        # self.setup(self.tmx_maps['ct7'], 'ct7', 'ufes') #ct7
        # self.setup(self.tmx_maps['sala_vitor'], 'sala_vitor', 'ct7') #sala_vitor
        # self.setup(self.tmx_maps['sala_monalessa'], 'sala_monalessa', 'ct7') #sala_monalessa
        # self.setup(self.tmx_maps['sala_patricia'], 'sala_patricia', 'ct7') #sala_patricia
        # self.setup(self.tmx_maps['ct9'], 'ct9', 'ufes') #ct9
        # self.setup(self.tmx_maps['labgrad'], 'labgrad', 'ct9') #labgrad
        # self.setup(self.tmx_maps['ending'], 'ending', 'ct7') #ending

        # Computer
        self.computer_links = []
        self.create_computer()

        # Inventory
        self.player_items = []
        self.create_inventory()

        # overlays
        self.dialog_open = None
        self.inventory = Inventory(self.player_items , self.fonts, self.interface_frames, self.sounds, self.item_used)
        self.inventory_open = False
        self.computer = Computer(self.computer_links,self.fonts, self.interface_frames, self.sounds)
        self.computer_open = False
        self.battle_open = False
        self.choose_dialog_open = False

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
        # clean all sprite groups
        for group in (self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites, self.collidable_dialogs_sprites, self.interaction_sprites):
            group.empty()
        # map theme
        self.audios[src_map].stop()
        self.audios[dest_map].play(-1)   

        # Terrenos
        try:
            for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])
        except ValueError as ve:
           pass

        # Coisas acima do terreno sem colisão
        try:
            for x, y, surf in tmx_map.get_layer_by_name('Terrain Top').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, GAME_LAYERS['bg'])
        except ValueError as ve:
           pass

        # Objetos em cima do terreno sem colisão (tapetes) 
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

        # dialogos só aparecem se o mapa não foi visitado anteriormente
        if (not tmx_map in VISITED_MAPS):
            VISITED_MAPS.append(tmx_map)
            # dialogos de colisão
            try:
                for obj in tmx_map.get_layer_by_name('Dialogs'):
                    CollidableDialogSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.collidable_dialogs_sprites), obj.properties['message'])
            except ValueError as ve:
               pass

        # transitions
        try:
            for obj in tmx_map.get_layer_by_name('Transitions'):
                TransitionSprite((obj.x, obj.y), obj.properties['dest'], obj.properties['src'], self.transition_sprites, (obj.width, obj.height))
        except ValueError as ve:
           pass

        # entities
        try:
            for obj in tmx_map.get_layer_by_name('Entities'):
                if obj.name == 'Player':
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
                        frames = self.overworld_frames['characters'][obj.properties['character_id']], 
                        facing_direction = obj.properties['direction'],
                        collision_sprites = self.collision_sprites,
                        character_data = CHARACTERS_DATA[obj.properties['character_id']],
                    )
        except ValueError as ve:
           pass
        if dest_map == 'ending':
            for character in self.character_sprites:
                character.character_data['end'] = True 

    # verifica a entrada do jogador
    def input(self):
        if not self.dialog_open and not self.choose_dialog_open and not self.battle_open:
            keys = pygame.key.get_just_pressed()
            # inventario
            if keys[pygame.K_i]:
                self.inventory_open = not self.inventory_open
                self.player.blocked = not self.player.blocked
                self.sounds['index_less'].play()
            # fechar sobreposições
            if keys[pygame.K_ESCAPE]:
                self.inventory_open = False
                self.computer_open = False
                self.player.blocked = False
                self.sounds['index_plus'].play()
            if keys[pygame.K_SPACE] and not self.dialog_open:
                self.check_dialog()
                # interações com objetos
                for sprite in self.interaction_sprites:
                    if check_interaction(150, self.player, sprite):
                        self.handle_interaction(sprite)

    # verifica se o player está interagindo com algum personagem
    def check_dialog(self):
        for character in self.character_sprites:
            if check_connections(100, self.player, character):
                character.change_facing_direction(self.player.rect.center)
                self.create_dialog(character)

    def handle_interaction(self, sprite):
        if sprite.item_id == 'computer':
            self.computer_open = not self.computer_open
            self.player.blocked = not self.player.blocked
            self.sounds['select'].play()
        if sprite.item_id == 'coffe':
            self.add_item(Item('4'))
            self.sounds['get_item'].play()
            sprite.kill()
        if sprite.item_id == 'abajour1':
            sprite.item_id = 'abajour2'
            sprite.image = self.interface_frames['interactive_objects']['abajour2']
        if sprite.item_id == 'abajour2':
            sprite.item_id = 'abajour1'
            sprite.image = self.interface_frames['interactive_objects']['abajour1']
        if sprite.item_id == 'geladeira1':
            sprite.item_id = 'geladeira2'
            sprite.image = self.interface_frames['interactive_objects']['geladeira2']
            self.add_item(Item('4'))
            self.sounds['get_item'].play()
        if sprite.item_id == 'geladeira2':
            sprite.item_id = 'geladeira1'
            sprite.image = self.interface_frames['interactive_objects']['geladeira1']
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
            self.create_dialog(self.player, "A placa diz: 'CT7 - Centro Tecnológico'...\n\nFinalmente cheguei! ", False)
        if sprite.item_id == 'placa_ct9':
            self.create_dialog(self.player, "A placa diz: 'CT9 - Centro Tecnológico'...\n\ntalvez eu deva estudar aqui antes do meu teste", False)
        if sprite.item_id == 'placa_ct10':
            self.create_dialog(self.player, "A placa diz: 'CT10 - Centro Tecnológico'...\n\nopa o ct9 é bem aqui", False)
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

    def item_used(self):
        self.player.speed_boost(1.5)
        self.buff_timer.activate()

    def create_dialog(self, character, message = None, collision_message = True):
        if not self.dialog_open:
            self.sounds['notice'].play()
            self.player.block()
            self.dialog_open = Dialog(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog, message, collision_message)

    # Callback functions
    # callback chamado ao final do dialogo
    # verifica se o personagem tem questões (se sim, vai para a batalha)
    # se não verifica se o pergonagem tem items para dar ao jogador
    def end_dialog(self,character):
        self.dialog_open = None
        # batalha
        if check_battle(character) and not self.battle_open and character.character_data['visited'] == False:
            self.player.block()
            # dialogo de escolha
            self.choose_dialog = ChooseDialog(character, self.interface_frames, self.fonts, self.end_choose_dialog)
            self.choose_dialog_open = True
        # item
        elif character.character_data['name'] != 'player' and character.character_data['visited'] != False and character.character_data['visited'] == True and character.character_data['item'] != None:
            self.sounds['get_item'].play()
            self.add_item(Item(character.character_data['item']))
            character.character_data['item'] = None
        if not self.choose_dialog_open:
            self.player.unblock()
            character.character_data['visited'] = True

    # callback chamado ao responder o dialogo de escolha
    # se o jogador escolher sim vai para a batalha
    # se o jogador escolher não, o personagem fala algo variando por qual for o professor
    def end_choose_dialog(self, answer, character):
        if answer:
            self.audios[self.current_map].stop()
            self.audios['battle'].play(-1)
            self.choose_dialog_open = False
            self.player.block()
            sleep(2)
            self.battle = Battle(self.player, character, self.interface_frames, self.fonts, self.end_battle, self.sounds)
            self.dialog_open = None
            self.battle_open = True
        else:
            if character.character_data['name'] == 'Vitor':
                self.create_dialog(character, "hahaha, veio de tão longe para arregar?", False)
            elif character.character_data['name'] == 'Monalessa':
                self.create_dialog(character, "volte quando estiver no meu nivel hehe", False)
            elif character.character_data['name'] == 'Patricia':
                self.create_dialog(character, "ta com medinho?",False)
            # self.dialog_open = None
            self.choose_dialog_open = False
            self.player.unblock()
        self.dialog_open = None

    # callback chamado ao final da batalha
    # verifica se o jogador acertou mais que 70% das perguntas
    # cria os links do computador com as perguntas erradas
    def end_battle(self, character, test):
        result = sum(test)
        sleep(2)
        self.audios['battle'].stop()
        self.audios[self.current_map].play(-1)
        self.battle_open = False
        text = 'voce acertou ' + str(result) + ' das ' + str(len(test))  + ' perguntas'
        if (result >= len(test) * 0.7): # 70% de acerto aprovado
            self.sounds['correct_answer'].play()
            character.character_data['visited'] = True
            self.create_dialog(character, text + '\ncheque no computador as questões que voce errou', False)
        else: # reprovado
            self.sounds['wrong_answer'].play()
            self.create_dialog(character, text + 'e foi REPROVADO\nvá no computador ver o que errou', False)
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
            elif transition_rect[0].dest == 'ending' and (not self.check_item(Item('0')) or not self.check_item(Item('1')) or not self.check_item(Item('2'))):
                self.sounds['51 - MMX - Can\'t Exit'].play()
            else:
                self.player.block()
                self.transition_area = transition_rect
                self.tint_mode = 'tint'

    # verifica se o player colidiu com uma caixa de dialogo
    def check_collidable_dialog(self):
        for sprite in self.collidable_dialogs_sprites:
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

    # função principal
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
            self.check_collidable_dialog()
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.player)

            # overlays
            if self.dialog_open: self.dialog_open.update()
            if self.inventory_open: self.inventory.update(dt)
            if self.computer_open: self.computer.update(dt)
            if self.battle_open: self.battle.update(dt)
            if self.choose_dialog_open: self.choose_dialog.update()
            # tint
            self.tint_screen(dt)
            pygame.display.update()

            # player buffs
            self.player_effects()
            self.buff_timer.update()

# Menu Inicial
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Super Labes World')

    home_open = True
    credits_open = False
    controls_open = False
    
    def run_game():
        global home_open; home_open = False

    def run_credits():
        global credits_open; credits_open = True
        global home_open; home_open = False

    def end_credits():
        global credits_open; credits_open = False
        global home_open; home_open = True

    def run_game_controls():
        global controls_open; controls_open = True
        global home_open; home_open = False

    def end_game_controls():
        global controls_open; controls_open = False
        global home_open; home_open = True


    home = Home(run_game,run_credits,run_game_controls)
    credits = Credits(end_credits)
    controls = GameControls(end_game_controls)

    while home_open or credits_open or controls_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif credits_open:
                credits.update()
            elif controls_open:
                controls.update()
            else:
                home.update()
            pygame.display.update()

    game = Game()
    game.run()


