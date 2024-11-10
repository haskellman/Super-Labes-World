import pygame
from support import import_folder_dict, audio_importer
from settings import *


class GameControls:
    def __init__(self, end_game_controls):    
        self.display_surface = pygame.display.get_surface()
        self.menu_frames = {'interface': import_folder_dict('.', 'graphics', 'interface') }
        self.sounds = audio_importer('.', 'sounds')
        self.index = 0
        self.end_game_controls = end_game_controls

    def draw_menu(self):
        self.index = self.index % 2
        back_rect = pygame.Rect(600,564,123,90)
        icon = self.menu_frames['interface']['voltar']
        self.display_surface.blit(self.menu_frames['interface']['game_controls_interface'])
        self.display_surface.blit(icon, back_rect, special_flags = pygame.BLEND_RGB_ADD)

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.sounds['select'].play()
            self.end_game_controls()

    
    def update(self):
        self.display_surface.fill(COLORS['black'])
        self.display_surface.blit(self.menu_frames['interface']['game_controls_interface'])
        self.input()
        self.draw_menu()

