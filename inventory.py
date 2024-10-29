from settings import * 
from game_data import CHARACTERS_DATA

class Inventory:
    def __init__(self, player_items, fonts, inventory_frames, player):
        self.fonts = fonts
        self.display_surface = pygame.display.get_surface()
        self.rows = 3
        self.col = 10
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 93
        self.x = (WINDOW_WIDTH - 968) / 2 
        self.y = (WINDOW_HEIGHT - 500) / 2
        self.border = 4
        self.index = 0
        self.selected_index = 0


        self.inventory_frames = inventory_frames['items'] 
        self.player_items = player_items
        self.inventory_bg = inventory_frames['bg']['inventory_bg']
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
                         (self.x,self.y,(self.box_size + self.border)*self.col + self.border,(self.box_size + self.border)*self.rows + self.border))
        for x in range(self.col):
            for y in range(self.rows): # celula
                index = x + y * self.col
                bg_color = COLORS['dark-brown']  if self.index != index else COLORS['mid-brown']
                self.rect = (self.x + (self.box_size + self.border)*x ,self.y + (self.box_size + self.border)*y,self.box_size, self.box_size)
                pygame.draw.rect(self.display_surface, bg_color ,self.rect)
                if self.player_items[index]:
                    if index == self.index:
                        self.display_surface.blit(self.player_items[index].item_icon, self.rect, special_flags = pygame.BLEND_RGB_MULT)
                    else:
                        self.display_surface.blit(self.player_items[index].item_icon, self.rect)

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
        image_rect = pygame.Rect(429,461,128,128)
        text_rect = pygame.Rect(565,461,432,128)
        pygame.draw.rect(self.display_surface,COLORS['white'],image_rect)
        pygame.draw.rect(self.display_surface,COLORS['dark-brown'],text_rect)
        if self.player_items[self.index]:
            self.display_surface.blit(pygame.transform.scale(self.player_items[self.index].item_icon,(image_rect.width,image_rect.height)), image_rect)
            text_surf = self.fonts['regular'].render(self.text_format(self.player_items[self.index].description), False, COLORS['black'])
            self.display_surface.blit(text_surf, text_rect)
        

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.index -= 10
        if keys[pygame.K_DOWN]:
            self.index += 10
        if keys[pygame.K_RIGHT]:
            self.index += 1
        if keys[pygame.K_LEFT]:
            self.index -= 1
        self.index = self.index % 30 # [LEN] voltar para o inicio
        if keys[pygame.K_SPACE]:
            if self.player_items[self.index] and self.player_items[self.index].name == 'cafe': # verificar se o item é utilizavel emitir um som
                self.player.speed += 1000
                self.player_items[self.index] = None # remove item

    def update(self, dt):
        self.input()
        self.display_surface.blit(self.tint_surface, (0,0))
        self.display_surface.blit(self.inventory_bg, (self.offset_bgx,self.offset_bgy))
        self.draw_items()
        self.draw_item_info()
