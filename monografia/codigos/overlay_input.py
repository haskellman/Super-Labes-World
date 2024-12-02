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
        self.index = self.index % self.inventory_size
        if keys[pygame.K_SPACE]:
            if self.player_items[self.index] and self.player_items[self.index].name == 'cafe':
                self.sounds['select'].play()
                self.player_items[self.index] = {}
                self.item_used()