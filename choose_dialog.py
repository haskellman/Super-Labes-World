from settings import * 

class ChooseDialog:
    def __init__(self, character, interface_frames, fonts, end_choose_dialog):
        
        self.interface_frames = interface_frames
        self.choose_bg = interface_frames['interface']['choose_interface']
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.character = character
        self.end_choose_dialog = end_choose_dialog
        self.rect_width = 310
        self.rect_height = 90

        # rectangles
        self.yes_rect = pygame.Rect(331, 577, self.rect_width, self.rect_height)
        self.no_rect = pygame.Rect(650, 577, self.rect_width, self.rect_height)
        self.question_rect = pygame.Rect(174, 385, 932, 145)

        # tint
        self.tint_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surface.set_alpha(180)   
        self.index = 0

    def draw_dialog(self):
        text_color = COLORS['black']
        text_rect = pygame.Rect(193,405,0,0)
        text = 'Você aceita o desafio do(a) ' + str(self.character.character_data['name']) +  ' ?'
        text_surf = self.fonts['regular_big'].render(text, False, text_color)
        self.display_surface.blit(text_surf, text_rect)
        if(self.index == 0):
            icon = self.interface_frames['interface']['sim']
            self.display_surface.blit(icon, self.yes_rect, special_flags = pygame.BLEND_RGB_ADD )
        elif(self.index == 1):
            icon = self.interface_frames['interface']['nao']
            self.display_surface.blit(icon, self.no_rect, special_flags = pygame.BLEND_RGB_ADD )

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.index = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.index = 1
        if keys[pygame.K_RETURN]:
            if self.index == 0:
                self.end_choose_dialog(True, self.character)
            elif self.index == 1:
                self.end_choose_dialog(False, self.character)

    def update(self):
        self.display_surface.blit(self.tint_surface)
        self.display_surface.blit(self.choose_bg)
        self.draw_dialog()
        self.input()
