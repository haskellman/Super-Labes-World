import pygame
from support import import_folder_dict, audio_importer, import_character
from settings import *
from random import randint, choice


ITEMS_FRAMES = ("down", "left", "right", "up")
class Home:
    def __init__(self, run_game, run_credits, run_game_controls):    
        self.initial_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_icon(pygame.image.load('icon.ico'))
        self.menu_frames = {'interface': import_folder_dict('.', 'graphics', 'interface') }
        self.fall_items = import_character(4, 4, '.', 'graphics', 'fall_objects', 'fall_objects')
        self.audios = audio_importer('.', 'audios')
        self.sounds = audio_importer('.', 'sounds')
        self.index = 0
        self.audios['opening'].play(-1)

        # movement
        self.x = 0
        self.y = 0
        self.speed = 10
        self.object_rect = pygame.Rect(randint(100, 1180), randint(-50, 0), 0, 0)
        self.object_surf = self.fall_items['down'][0]
        self.fall_objects_list = self.generate_list_fall_objects()

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

    def fall_objects(self):  
        self.object_rect.y += self.move_y(self.speed)
        for rect, surf in self.fall_objects_list:
            rect.y += self.speed
            self.initial_screen.blit(surf, rect)
            if rect.y > WINDOW_HEIGHT:
                self.fall_objects_list.remove((rect, surf))
                self.fall_objects_list.append(self.generate_fall_objects())

    def generate_fall_objects(self):
        random = randint(0, 360)
        return pygame.Rect(randint(50, WINDOW_WIDTH - 50), randint(-500, 0), 0, 0), pygame.transform.rotate(self.fall_items[choice(ITEMS_FRAMES)][random % 4], random)
    
    def generate_list_fall_objects(self):
        return [self.generate_fall_objects() for _ in range(10)]
    
    def move_y(self, speed):
        if True:
            self.y += speed
            if self.object_rect.y > WINDOW_HEIGHT:
                self.object_rect, self.object_surf = self.generate_fall_objects()
        return self.y

    def update(self):
        self.initial_screen.blit(self.menu_frames['interface']['opening_interface'])
        self.draw_menu()
        # self.fall_objects()
        self.input()

