# Menu Inicial
import pygame
from game import Game
from home import Home
from credits import Credits

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Super Labes World')

    home_open = True
    credits_open = False
    controls_open = False

    home = Home(run_game,run_credits,run_game_controls)
    credits = Credits(end_credits)
    controls = GameControls(end_game_controls)

    while home_open or credits_open or controls_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif credits_open:
                credits.update()
            elif controls_open:
                controls.update()
            else:
                home.update()
            pygame.display.update()

    game = Game()
    game.run()