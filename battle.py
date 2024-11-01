from settings import * 

class Battle():
    def __init__(self, player, character, interface_frames, fonts):
        self.player = player
        self.character = character
        self.max_option = 4
        self.option = 0
        self.interface_frames = interface_frames
        self.battle_bg = interface_frames['interface']['battle_interface']
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.rows = 2
        self.cols = 2
        self.rect_width = 310
        self.rect_height = 90
        
        self.option_rect = pygame.Rect(75,568,504,125)
        self.questions = self.character.questions
        self.qtd_questions = len(self.questions)
        self.current_question = 0
        self.current_question_dict = self.questions[self.current_question].values()
        self.icon = self.interface_frames['interface'][str(self.option)]

        self.correct_answer = self.get_correct_answer(self.current_question_dict)



    def draw(self):
        text_color = COLORS['black']

        # rectangles
        rect_A = pygame.Rect(632, 540, self.rect_width, self.rect_height)
        rect_B = pygame.Rect(942, 540, self.rect_width, self.rect_height)
        rect_C = pygame.Rect(632, 630, self.rect_width, self.rect_height)
        rect_D = pygame.Rect(942, 630, self.rect_width, self.rect_height)
        question_rect = pygame.Rect(608, 4, self.rect_width, self.rect_height)
        

        # surfaces
        text_surf = self.fonts['regular'].render(self.get_options(self.current_question_dict), False, text_color)
        question_surf = self.fonts['regular'].render(self.get_question(self.current_question_dict), False, text_color)
        print(self.get_question(self.current_question_dict))

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
        # print(self.get_correct_answer(self.current_question_dict))

    def get_options(self,text_dict):
        new_text = []
        values_list = list(text_dict)
        new_text.append(values_list[2][self.option] + ':\n')
        return ''.join(new_text)
    
    def get_question(self, text_dict):
        new_text = []
        values_list = list(text_dict)
        new_text.append(values_list[0] + ':\n')
        new_text.append(values_list[1] + '\n')
        return ''.join(new_text)

    def get_correct_answer(self, text_dict):
        values_list = list(text_dict)
        return values_list[3]

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
           self.option -= 2
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
           self.option += 2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
           self.option += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
           self.option -= 1
        self.option =self.option % self.max_option
        if keys[pygame.K_SPACE]:
            self.current_question += 1
            print(self.current_question)
            if self.current_question == self.correct_answer:
                print('Acertou')


    def update(self, dt):
        self.input()
        self.display_surface.blit(self.battle_bg)
        self.draw()
