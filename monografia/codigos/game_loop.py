import pygame

def run(self):
        # event loop
        while True:
            self.screen.fill(COLORS['black'])
            dt = self.clock.tick() / 1000 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic
            self.input()
            self.check_transitions()
            self.check_dialog()
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.player)

            # overlays
            if self.dialog_open: self.dialog_open.update()
            if self.inventory_open: self.inventory.update(dt)
            if self.computer_open: self.computer.update(dt)
            if self.battle_open: self.battle.update(dt)
            if self.choose_dialog_open: self.choose_dialog.update()

            # tint
            self.tint_screen(dt)
            # self.tint_battle(dt)
            pygame.display.update()

            # player buffs
            self.player_effects()
            self.buff_timer.update()