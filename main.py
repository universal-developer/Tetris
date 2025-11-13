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

    # Match window size exactly to BaseTetris layout (with top margin)
    cols, rows, cell_size = 10, 20, 30
    top_margin = 56  # same as in BaseTetris
    width = cols * cell_size + 40
    height = rows * cell_size + 80 + top_margin

    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tetris Menu")

    # Create menu with consistent dimensions and a clean dark look
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame.font.SysFont("arial", 36, bold=True)
    theme.widget_font = pygame.font.SysFont("arial", 26)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    theme.background_color = (15, 15, 15)
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    menu = pygame_menu.Menu(
        title='TETRIS',
        width=width,
        height=height,
        theme=theme
    )

    # Centered, balanced menu buttons
    menu.add.button('Tetris Normal', start_normal)
    menu.add.button('Tetris Inversé', start_inverted)
    menu.add.button('Quitter', pygame_menu.events.EXIT)

    menu.mainloop(surface)
    pygame.quit()


if __name__ == "__main__":
    main()
