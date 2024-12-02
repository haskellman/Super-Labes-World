
class Home:
    def __init__(self, run_game, run_credits, run_game_controls):    
        self.initial_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # callbacks
        self.run_game = run_game
        self.run_credits = run_credits
        self.run_game_controls = run_game_controls

    def draw_menu(self):
        self.index = self.index % 4
        if self.index == 0:
            new_rect = pygame.Rect(226,564,123,90)
            icon = self.menu_frames['interface']['new']
        elif self.index == 1:
            new_rect = pygame.Rect(464,564,123,90)
            icon = self.menu_frames['interface']['credits']
        elif self.index == 2:
            new_rect = pygame.Rect(700,564,123,90)
            icon = self.menu_frames['interface']['controles']
        else:
            new_rect = pygame.Rect(936,564,123,90)
            icon = self.menu_frames['interface']['exit']
        icon = self.menu_frames['interface']['new'] if self.index == 0 else self.menu_frames['interface']['credits'] if self.index == 1 else self.menu_frames['interface']['controles'] if self.index == 2 else self.menu_frames['interface']['exit']
        self.initial_screen.blit(self.menu_frames['interface']['opening_interface'])
        self.initial_screen.blit(icon, new_rect, special_flags = pygame.BLEND_RGB_ADD)

    def update(self):
        self.initial_screen.blit(self.menu_frames['interface']['opening_interface'])
        self.draw_menu()
        self.input()

