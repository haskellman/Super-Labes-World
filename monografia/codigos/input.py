# verifica a entrada do jogador
def input(self):
    if not self.dialog_open and not self.choose_dialog_open and not self.battle_open:
        keys = pygame.key.get_just_pressed()
        # inventario
        if keys[pygame.K_i]:
            self.inventory_open = not self.inventory_open
            self.player.blocked = not self.player.blocked
            self.sounds['index_less'].play()
        # fechar sobreposições
        if keys[pygame.K_ESCAPE]:
            self.inventory_open = False
            self.computer_open = False
            self.player.blocked = False
            self.sounds['index_plus'].play()
        if keys[pygame.K_SPACE] and not self.dialog_open:
            self.check_dialog()
            # interações com objetos
            for sprite in self.interaction_sprites:
                if check_interaction(150, self.player, sprite):
                    self.handle_interaction(sprite)