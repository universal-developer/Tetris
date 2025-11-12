import pygame
import pygame_menu
from normal_tetris import Game as NormalGame
from inverted_tetris import Game as InvertedGame

def start_normal():
    NormalGame().run()

def start_inverted():
    InvertedGame().run()

def main():
    pygame.init()
    surface = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("Tetris Menu")

    menu = pygame_menu.Menu('Tetris Modes', 400, 500, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Tetris Normal', start_normal)
    menu.add.button('Tetris Inversé', start_inverted)
    menu.add.button('Quitter', pygame_menu.events.EXIT)

    menu.mainloop(surface)
    pygame.quit()

if __name__ == "__main__":
    main()
