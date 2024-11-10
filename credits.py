import pygame
from support import import_folder_dict, audio_importer
from settings import *
import webbrowser


class Credits:
    def __init__(self, end_credits):    
        self.display_surface = pygame.display.get_surface()
        self.menu_frames = {'interface': import_folder_dict('.', 'graphics', 'interface') }
        self.sounds = audio_importer('.', 'sounds')
        self.index = 0
        self.end_credits = end_credits


    def draw_menu(self):
        self.index = self.index % 2
        new_rect = pygame.Rect(236,29,807,306) if self.index == 0 else pygame.Rect(600,564,123,90)
        icon = self.menu_frames['interface']['github'] if self.index == 0 else self.menu_frames['interface']['voltar']
        self.display_surface.blit(self.menu_frames['interface']['credits_interface'])
        self.display_surface.blit(icon, new_rect, special_flags = pygame.BLEND_RGB_ADD)
        # pygame.display.update()

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.sounds['index_plus'].play()
            self.index += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.sounds['index_less'].play()
            self.index -= 1
        if self.index == 0 and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
            self.sounds['select'].play()
            webbrowser.open('https://github.com/haskellman', new=0, autoraise=True)
        if self.index == 1 and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
            self.sounds['select'].play()
            self.end_credits()

    
    def update(self):
        self.display_surface.fill(COLORS['black'])
        self.display_surface.blit(self.menu_frames['interface']['credits_interface'])
        self.input()
        self.draw_menu()
        print(self.index)

