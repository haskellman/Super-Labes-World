from settings import * 
from entities import Player

class Inventory:
    def __init__(self, player_items, fonts, interface_frames, player, sounds, item_used):
        self.fonts = fonts
        self.display_surface = pygame.display.get_surface()
        self.rows = 3
        self.cols = 10
        self.items = [[None for _ in range(self.rows)] for _ in range(self.cols)]
        self.box_size = 93
        self.x = (WINDOW_WIDTH - 968) / 2 
        self.y = (WINDOW_HEIGHT - 500) / 2
        self.border = 4
        self.index = 0
        self.selected_index = 0
        self.inventory_size = 30
        self.sounds = sounds
        self.item_used = item_used

        self.player_items = player_items
        self.inventory_bg = interface_frames['interface']['inventory_interface']
        self.player = player

        self.offset_bgx = (WINDOW_WIDTH - self.inventory_bg.width) / 2
        self.offset_bgy = (WINDOW_HEIGHT- self.inventory_bg.height) / 2

        # tint
        self.tint_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surface.set_alpha(180)


    #draw everything
    def draw_items(self):
        #draw background
        pygame.draw.rect(self.display_surface,COLORS['brown'],
                         (self.x,self.y,(self.box_size + self.border)*self.cols + self.border,(self.box_size + self.border)*self.rows + self.border))
        for x in range(self.cols):
            for y in range(self.rows): # celula
                index = x + y * self.cols
                bg_color = COLORS['dark-brown']  if self.index != index else COLORS['mid-brown']
                self.rect = (self.x + (self.box_size + self.border)*x ,self.y + (self.box_size + self.border)*y,self.box_size, self.box_size)
                pygame.draw.rect(self.display_surface, bg_color ,self.rect)
                if self.player_items[index]:
                    if index == self.index:
                        self.display_surface.blit(self.player_items[index].icon, self.rect, special_flags = pygame.BLEND_RGB_MULT)
                    else:
                        self.display_surface.blit(self.player_items[index].icon, self.rect)

    def text_format(self,text):
        new_text = []
        count = 0
        for c in text:
            count += 1
            new_text.append(c)
            if c == '\n':
                count = 0	
            if count % 41 == 0:
                new_text.append('\n')

        
        return ''.join(new_text)
    
    def draw_item_info(self):
        # rectangles
        item_name_rect = pygame.Rect(384, 458, 0, 0)
        image_rect = pygame.Rect(404,477,128,128)
        description_rect = pygame.Rect(565,461,432,128)
        pygame.draw.rect(self.display_surface,COLORS['white'],image_rect)
        if self.player_items[self.index]:
            # texts
            item_name_surf = self.fonts['regular'].render(self.player_items[self.index].name, False, COLORS['black'])
            description_surf = self.fonts['regular'].render(self.text_format(self.player_items[self.index].description), False, COLORS['black'])
            # draw
            self.display_surface.blit(pygame.transform.scale(self.player_items[self.index].icon,(image_rect.width,image_rect.height)), image_rect)
            self.display_surface.blit(description_surf, description_rect)
            self.display_surface.blit(item_name_surf, item_name_rect)
        

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.index -= 10
            self.play_sound()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.index += 10
            self.play_sound()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.index += 1
            self.play_sound()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.index -= 1
            self.play_sound()
        self.index = self.index % self.inventory_size # [LEN] voltar para o inicio
        if keys[pygame.K_SPACE]:
            if self.player_items[self.index] and self.player_items[self.index].name == 'cafe': # verificar se o item é utilizavel emitir um som
                self.sounds['item_used'].play()
                self.player_items[self.index] = {} # remove item
                self.item_used()

    def play_sound(self):
        self.sounds['inventory_select'].play()

    def update(self, dt):
        self.input()
        self.display_surface.blit(self.tint_surface, (0,0))
        self.display_surface.blit(self.inventory_bg)
        self.draw_items()
        self.draw_item_info()
