
class Home:
    def __init__(self, run_game, run_credits, run_game_controls):    
        self.initial_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.menu_frames = {'interface': import_folder_dict('.', 'graphics', 'interface') }
        self.audios = audio_importer('.', 'audios')
        self.sounds = audio_importer('.', 'sounds')
        self.index = 0
        self.audios['opening'].play(-1)
        
        # callbacks
        self.run_game = run_game
        self.run_credits = run_credits
        self.run_game_controls = run_game_controls

    def draw_menu(self):
        self.index = self.index % 4
        new_rect = pygame.Rect(226,564,123,90) if self.index == 0 else pygame.Rect(464,564,123,90) if self.index == 1 else pygame.Rect(700,564,123,90) if self.index == 2 else pygame.Rect(936,564,123,90)
        icon = self.menu_frames['interface']['new'] if self.index == 0 else self.menu_frames['interface']['credits'] if self.index == 1 else self.menu_frames['interface']['controles'] if self.index == 2 else self.menu_frames['interface']['exit']
        self.initial_screen.blit(self.menu_frames['interface']['opening_interface'])
        self.initial_screen.blit(icon, new_rect, special_flags = pygame.BLEND_RGB_ADD)

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_RIGHT]:
            self.sounds['index_plus'].play()
            self.index += 1
        if keys[pygame.K_LEFT]:
            self.sounds['index_less'].play()
            self.index -= 1
        if self.index == 0 and keys[pygame.K_RETURN]:
            self.sounds['select'].play()
            self.audios['opening'].stop()
            self.run_game()
        if self.index == 1 and keys[pygame.K_RETURN]:
            self.sounds['select'].play()
            self.run_credits()
        if self.index == 2 and keys[pygame.K_RETURN]:
            self.sounds['select'].play()
            self.run_game_controls()
        if self.index == 3 and keys[pygame.K_RETURN]:
            pygame.quit()
            exit()

    def update(self):
        self.initial_screen.blit(self.menu_frames['interface']['opening_interface'])
        self.draw_menu()
        self.input()

