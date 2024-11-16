from settings import * 
from time import sleep
from timer import Timer
from support import import_image
from dialog import DialogSprite
from game_data import CORRECTS_SPEAKS, WRONGS_SPEAKS

class Battle():
    def __init__(self, player, character, interface_frames, fonts, end_battle, sounds):
        self.player = player
        self.character = character
        self.interface_frames = interface_frames
        self.battle_bg = interface_frames['interface']['battle_interface']
        self.character_frames = character.frames
        self.player_frames = import_image('.', 'graphics', 'characters', 'player_battle')
        self.fonts = fonts
        self.end_battle = end_battle
        self.sounds = sounds
        self.display_surface = pygame.display.get_surface()
        self.battle_timer = Timer(1, autostart = True)
        self.test = []
        self.shadow = import_image('.', 'graphics', 'shadow', 'shadow')

        self.frame_index = 0
        self.rows = 2
        self.cols = 2
        self.option = 0
        self.rect_width = 310
        self.rect_height = 90
        
        self.option_rect = pygame.Rect(75,568,504,125)
        self.questions = self.character.questions
        self.qtd_questions = len(self.questions)
        self.current_question = 0
        self.answer = -1

        # animation
        self.x = 0
        self.y = 0
        self.move_horizontal = True
        self.move_vertical = False
        self.error_mode = False

        # speak
        self.character_rect = pygame.Rect(853, 137, 192, 192)
        self.counter_text_speak = 0
        self.speed_text_speak = 300
        self.done_text_speak = False
        self.speak_rect = pygame.Rect(756, 29, 421, 99)


    def draw(self, dt):
        if self.current_question != self.qtd_questions:
            text_color = COLORS['black']
            current_question_dict = self.questions[self.current_question].values()
            current_answer = self.get_correct_answer(current_question_dict)

            self.answer = current_answer

            # rectangles
            rect_A = pygame.Rect(632, 540, self.rect_width, self.rect_height)
            rect_B = pygame.Rect(942, 540, self.rect_width, self.rect_height)
            rect_C = pygame.Rect(632, 630, self.rect_width, self.rect_height)
            rect_D = pygame.Rect(942, 630, self.rect_width, self.rect_height)
            question_rect = pygame.Rect(93, 29, 421, 99)
            name_rect = pygame.Rect(838, 370, 0, 0)
            level_rect = pygame.Rect(844, 396, 0, 0)

            self.icon = self.interface_frames['interface'][str(self.option)]
            # player
            player_surf = self.player_frames
            
            # movement
            if self.current_question > 0:
                if self.current_question < self.qtd_questions / 3:
                    self.frame_index += ANIMATION_SPEED * dt 
                    self.x = self.move_x(dt, 30, 30)
                    self.y = self.move_y(dt, 50, 30)
                elif self.current_question < self.qtd_questions / 2 + 1:
                    self.frame_index += 2 * ANIMATION_SPEED * dt 
                    self.x = self.move_x(dt, 60, 35)
                    self.y = self.move_y(dt, 100, 35)
                elif self.current_question < self.qtd_questions / 2 + 3:
                    self.frame_index += 3 * ANIMATION_SPEED * dt 
                    self.x = self.move_x(dt, 90, 40)
                    self.y = self.move_y(dt, 150, 40)
                else: # 9 e 10
                    self.frame_index += 4 * ANIMATION_SPEED * dt 
                    self.x = self.move_x(dt, 120, 50)
                    self.y = self.move_y(dt, 200, 50)

            # character animation
            self.character_rect = pygame.Rect(853 + self.x, 137 + self.y, 192, 192)
            character_surf = self.character_frames['up' if self.error_mode else 'left'][int(self.frame_index % 4)] # animation

            # teacher character 
            self.display_surface.blit(pygame.transform.scale(character_surf,(192,192)), self.character_rect)
            # shadow
            self.display_surface.blit(pygame.transform.scale(self.shadow, (78,30)), self.character_rect.midbottom + vector(-36,-20))
            # player character
            self.display_surface.blit(player_surf, (148 + (self.x // 3), 284))

            # surfaces
            text_surf = self.fonts['regular'].render(self.get_options(current_question_dict), False, text_color)
            question_surf = self.fonts['regular'].render(self.get_question(current_question_dict), False, text_color)
            name_surf = self.fonts['regular_mid'].render(self.character.character_data['name'], False, text_color)
            level_surf = self.fonts['regular_mid'].render('??????', False, text_color)

            # draw
            if(self.option == 0):
                self.display_surface.blit(self.icon, rect_A, special_flags = pygame.BLEND_RGB_ADD )
            elif(self.option == 1):
                self.display_surface.blit(self.icon, rect_B, special_flags = pygame.BLEND_RGB_ADD )
            elif(self.option == 2):
                self.display_surface.blit(self.icon, rect_C, special_flags = pygame.BLEND_RGB_ADD )
            elif(self.option == 3):
                self.display_surface.blit(self.icon, rect_D, special_flags = pygame.BLEND_RGB_ADD )
            self.display_surface.blit(text_surf, self.option_rect)
            self.display_surface.blit(question_surf, question_rect)
            self.display_surface.blit(name_surf, name_rect)
            self.display_surface.blit(level_surf, level_rect)

    def move_x(self, dt, speed, range):
        if not self.error_mode:
            if self.move_horizontal:
                self.x += speed * dt
                if self.x > range:
                    self.move_horizontal = False
            else:
                self.x -= speed * dt
                if self.x < 0:
                    self.move_horizontal = True
        return self.x
    
    def move_y(self, dt, speed, range):
        if self.error_mode:
            if self.move_vertical:
                self.y += speed * dt
                if self.y > range:
                    self.move_vertical = False
            else:
                self.y -= speed * dt
                if self.y < 0:
                    self.move_vertical = True
        return self.y


    def get_options(self,text_dict):
        new_text = []
        values_list = list(text_dict)
        new_text.append(self.text_format(values_list[2][self.option],48))
        return ''.join(new_text)
    
    def get_question(self, text_dict):
        new_text = []
        values_list = list(text_dict)
        new_text.append(values_list[0] + ':\n') # title
        new_text.append (self.text_format(values_list[1],40)) # question
        return ''.join(new_text)
    
    def text_format(self, text, size):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) <= size:
                current_line += word + " "
            else:
                lines.append(current_line + '\n')
                current_line = word + " "
        lines.append(current_line)
        return ''.join(lines)

    def get_correct_answer(self, text_dict):
        values_list = list(text_dict)
        return values_list[3]

    def input(self):
        keys = pygame.key.get_just_pressed()
        if not self.battle_timer.active:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.option -= 2
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.option += 2
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.option += 1
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.option -= 1
            self.option =self.option % 4
            if keys[pygame.K_RETURN]:
                self.battle_timer.activate()
                self.current_question += 1
                self.check_answer()
                
    # checagem da resposta
    def check_answer(self):
        if self.option == self.answer:
            self.test.append(1)
            self.error_mode = False
            self.sounds['correct_answer'].play()
            self.counter_text_speak = 0
            self.done_text_speak = False

        else:
            self.test.append(0)
            self.error_mode = True
            self.sounds['wrong_answer'].play()
            self.counter_text_speak = 0
            self.done_text_speak = False

    def check_end_battle(self):
        if self.current_question == self.qtd_questions:
            self.end_battle(self.character, self.test)

    def draw_dialog(self, dt):
        # quando a pessoa erra o personagem fala um dos dialogos de erro
        if self.error_mode:
            text = self.text_format(WRONGS_SPEAKS[self.current_question], 30)
            if self.counter_text_speak < len(WRONGS_SPEAKS[self.current_question]) * self.speed_text_speak:
                self.counter_text_speak += int(5000 * dt)
            elif self.counter_text_speak >= len(WRONGS_SPEAKS[self.current_question]) * self.speed_text_speak:
                self.done_text_speak = True
            text_surf = self.fonts['regular'].render(text[0:self.counter_text_speak//self.speed_text_speak], True, COLORS['black'])
            self.display_surface.blit(text_surf, self.speak_rect)

        # quando a pessoa acerta o personagem fala o dialogo de acerto
        else:
            text = self.text_format(CORRECTS_SPEAKS[self.current_question], 30)
            if self.counter_text_speak < len(CORRECTS_SPEAKS[self.current_question]) * self.speed_text_speak:
                self.counter_text_speak += int(5000 * dt)
            elif self.counter_text_speak >= len(CORRECTS_SPEAKS[self.current_question]) * self.speed_text_speak:
                self.done_text_speak = True                
            text_surf = self.fonts['regular'].render(CORRECTS_SPEAKS[self.current_question][0:self.counter_text_speak//self.speed_text_speak], True, COLORS['black'])
            self.display_surface.blit(text_surf, self.speak_rect)  

    def update(self, dt):
        self.battle_timer.update()
        self.check_end_battle()
        self.input()
        self.display_surface.blit(self.battle_bg)
        self.draw(dt)
        self.draw_dialog(dt)
