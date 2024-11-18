# verifica a entrada do jogador
def input(self):
    if not self.dialog_open and not self.choose_dialog_open and not self.battle_open:
        keys = pygame.key.get_just_pressed()
        # inventario
        if keys[pygame.K_i]:
            self.inventory_open = not self.inventory_open
            self.player.blocked = not self.player.blocked
            # emitir som
        # fechar sobreposições
        if keys[pygame.K_ESCAPE]:
            self.inventory_open = False
            self.computer_open = False
            self.player.blocked = False
        if keys[pygame.K_SPACE] and not self.dialog_open:
            # interações com personagens
            for character in self.character_sprites:
                if check_connections(100, self.player, character):
                    character.change_facing_direction(self.player.rect.center)
                    self.create_dialog(character)

            # interações com objetos
            for sprite in self.interaction_sprites:
                if check_interaction(150, self.player, sprite):
                    if sprite.item_id == 'computer':
                        self.computer_open = not self.computer_open
                        self.player.blocked = not self.player.blocked
                        break