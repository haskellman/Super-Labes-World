    def draw_characters(self, dt):
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
            else:
                self.frame_index += 4 * ANIMATION_SPEED * dt 
                self.x = self.move_x(dt, 120, 50)
                self.y = self.move_y(dt, 200, 50)

        # character movement
        self.character_rect = pygame.Rect(853 + self.x, 137 + self.y, 192, 192)
        self.player_rect = pygame.Rect(148 + (self.x // 3), 284, 192, 192)
        # character animation
        character_surf = self.character_frames['up' if self.error_mode else 'left'][int(self.frame_index % 4)] 
        # player
        player_surf = self.player_frames
        # draw
        self.display_surface.blit(pygame.transform.scale(character_surf,(192,192)), self.character_rect)
        self.display_surface.blit(pygame.transform.scale(self.shadow, (78,30)), self.character_rect.midbottom + vector(-36,-20))
        self.display_surface.blit(player_surf, self.player_rect)