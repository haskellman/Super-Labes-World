class Game:
    def __init__(self): 
        # inicialização
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.buff_timer = Timer(15000, autostart = True) # 15 segundos
        
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

        # importação de todos os assets
        self.import_assets()

        # audios e efeitos sonoros
        self.current_map = 'house'
        self.audios = audio_importer('.', 'audios')
        self.sounds = audio_importer('.', 'sounds')

        # mapa iniciais
        self.setup(self.tmx_maps['house'], 'house', 'house') #house

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