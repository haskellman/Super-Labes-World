class Game:
    def __init__(self): 
        ... inicialização de variáveis 
        ... inicialização de audios

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites   = pygame.sprite.Group()
        self.character_sprites   = pygame.sprite.Group()
        self.transition_sprites  = pygame.sprite.Group()
        self.collidable_dialogs_sprites     = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        
        # importação de todos os assets
        self.import_assets()

        # inicialização do mapa
        self.setup(self.tmx_maps['house'], 'house', 'house') #house

        # overlays
        self.dialog_open = None
        self.inventory = Inventory(self.player_items , self.fonts, self.interface_frames, self.sounds, self.item_used)
        self.inventory_open = False
        self.computer = Computer(self.computer_links,self.fonts, self.interface_frames, self.sounds)
        self.computer_open = False
        self.battle_open = False
        self.choose_dialog_open = False