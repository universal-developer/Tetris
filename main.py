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

    # Match window size to Tetris grid (10 cols × 30px + margins, 20 rows × 30px + margins)
    cols, rows, cell_size = 10, 20, 30
    width = cols * cell_size + 40
    height = rows * cell_size + 80

    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tetris Menu")

    # Create menu with same size and theme
    menu = pygame_menu.Menu(
        'Tetris Modes',
        width,
        height,
        theme=pygame_menu.themes.THEME_DARK
    )

    # Add buttons
    menu.add.button('Tetris Normal', start_normal)
    menu.add.button('Tetris Inversé', start_inverted)
    menu.add.button('Quitter', pygame_menu.events.EXIT)

    menu.mainloop(surface)
    pygame.quit()

if __name__ == "__main__":
    main()
