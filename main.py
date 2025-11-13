import pygame
import pygame_menu
from normal_tetris import Game as NormalGame
from inverted_tetris import Game as InvertedGame
from regle_tetris import Presentation as RegleDuJeu


def start_regle():
    """Affiche la fenêtre des règles du jeu."""
    RegleDuJeu().run()

    # --- Réinitialiser la taille d’affichage du menu ---
    cols, rows, cell_size = 10, 20, 30
    top_margin = 56
    width = cols * cell_size + 40
    height = rows * cell_size + 80 + top_margin
    pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tetris Menu")


def start_normal():
    NormalGame(False).run()


def start_inverted():
    InvertedGame().run()


def start_fou_game():
    NormalGame(True).run()


def main():
    pygame.init()

    # --- Même taille que la fenêtre du jeu ---
    cols, rows, cell_size = 10, 20, 30
    top_margin = 56  # même valeur que dans BaseTetris
    width = cols * cell_size + 40
    height = rows * cell_size + 80 + top_margin

    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tetris Menu")

    # --- Crée un menu simple ---
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame.font.SysFont("arial", 36, bold=True)
    theme.widget_font = pygame.font.SysFont("arial", 26)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    theme.background_color = (20, 20, 20)
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    menu = pygame_menu.Menu(
        title="TETRIS",
        width=width,
        height=height,
        theme=theme
    )

    # --- Boutons du menu ---
    menu.add.button("Règles du jeu", start_regle)
    menu.add.button("Tetris Normal", start_normal)
    menu.add.button("Tetris Inversé", start_inverted)
    menu.add.button("Tetris Fou", start_fou_game)
    menu.add.button("Quitter", pygame_menu.events.EXIT)

    # --- Boucle principale ---
    menu.mainloop(surface)


if __name__ == "__main__":
    main()


