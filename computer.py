from settings import * 
import webbrowser


class Computer:
    def __init__(self, computer_links, fonts, interface_frames, sounds):
        self.fonts = fonts
        self.display_surface = pygame.display.get_surface()
        self.rows = len(computer_links) if len(computer_links) > 0 else 1 # correção de divisão por zero
        self.visible_items = 3
        self.index = 0
        self.rect = pygame.Rect(192,176, 608, 108)

        # dimensions
        self.main_rect = pygame.FRect(192,176, 608, 336)
        self.list_width = self.main_rect.width
        self.item_height = self.main_rect.height / self.visible_items

        self.computer_bg = interface_frames['interface']['computer_interface']
        self.computer_links = computer_links
        self.sounds = sounds

        # tint
        self.tint_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surface.set_alpha(180)        

    def draw_items(self):
        bg_rect = self.main_rect
        pygame.draw.rect(self.display_surface, COLORS['gray'], bg_rect)

        v_offset = 0 if self.index < self.visible_items else -(self.index - self.visible_items + 1) * self.item_height
        for index, value in enumerate(self.computer_links):
            bg_color = COLORS[self.computer_links[index].color] if self.index != index else COLORS['light']
            text_color = COLORS['white'] if bg_color != COLORS['white'] else COLORS['black']

            top = self.main_rect.top + index * self.item_height + v_offset

            item_rect = pygame.FRect(self.main_rect.left,top,self.list_width,self.item_height)

            text_surf = self.fonts['regular'].render(self.text_format(self.computer_links[index]), False, text_color)
            text_rect = text_surf.get_frect(midleft = item_rect.midleft + vector(120, 0))

            icon_surf = self.computer_links[index].icon
            icon_rect = icon_surf.get_frect(center = item_rect.midleft + vector(60,0))

            if item_rect.colliderect(self.main_rect):
                # check corners
                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)
                elif item_rect.collidepoint(self.main_rect.bottomleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)

                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)

            # lines 
            for i in range(1, min(self.visible_items, len(self.computer_links))):
                y = self.main_rect.top + self.item_height * i
                left = self.main_rect.left
                right = self.main_rect.left + self.list_width
                pygame.draw.line(self.display_surface, COLORS['light-gray'], (left, y), (right, y))

    def text_format(self,text):
        new_text = []
        new_text.append(text.title + ':\n')
        count = 0
        max_characters = 0 
        for c in text.description:
            count += 1
            max_characters += 1
            new_text.append(c)
            if c == '\n':
                count = 0	
            if count % 46 == 0:
                new_text.append('\n')
            if max_characters > 130:
                new_text.append('...')
                break        
        return ''.join(new_text)
                
    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.play_sound()
            self.index -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.play_sound()
            self.index += 1
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.play_sound()
            webbrowser.open(self.computer_links[self.index].url, new=0, autoraise=True)
        self.index = self.index % self.rows # [LEN] voltar para o inicio

    def play_sound(self):
        self.sounds['inventory_select'].play()

    def update(self, dt):
        self.input()
        self.display_surface.blit(self.tint_surface)
        self.display_surface.blit(self.computer_bg)
        self.draw_items()


