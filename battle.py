from settings import * 
from time import sleep
from timer import Timer
class Battle():
    def __init__(self, player, character, interface_frames, fonts, end_battle, sounds):
        self.player = player
        self.character = character
        self.interface_frames = interface_frames
        self.battle_bg = interface_frames['interface']['battle_interface']
        self.frames = character.frames
        self.fonts = fonts
        self.end_battle = end_battle
        self.sounds = sounds
        self.display_surface = pygame.display.get_surface()
        self.battle_timer = Timer(2000, autostart = True)
        self.test = []

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
            question_rect = pygame.Rect(756, 29, 421, 99)
            self.icon = self.interface_frames['interface'][str(self.option)]

            # character
            character_surf = self.frames['down_idle'][0]
            character_rect = pygame.Rect(853, 137, 0, 0)
            self.display_surface.blit(pygame.transform.scale(character_surf,(192,192)), character_rect)

            # surfaces
            text_surf = self.fonts['regular'].render(self.get_options(current_question_dict), False, text_color)
            question_surf = self.fonts['regular'].render(self.get_question(current_question_dict), False, text_color)

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

    def get_options(self,text_dict):
        new_text = []
        values_list = list(text_dict)
        new_text.append(values_list[2][self.option] + ':\n')
        return ''.join(new_text)
    
    def get_question(self, text_dict):
        new_text = []
        values_list = list(text_dict)
        new_text.append(values_list[0] + ':\n') # title
        new_text.append (self.text_format(values_list[1])) # question
        return ''.join(new_text)
    
    def text_format(self, text):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) <= 40:
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
                if self.option == self.answer:
                    self.test.append(1)
                    self.sounds['correct_answer'].play()
                else:
                    self.test.append(0)
                    self.sounds['wrong_answer'].play()

    def check_end_battle(self):
        if self.current_question == self.qtd_questions:
            self.end_battle(self.character, self.test)


    def update(self, dt):
        self.battle_timer.update()
        self.check_end_battle()
        self.input()
        self.display_surface.blit(self.battle_bg)
        self.draw(dt)
