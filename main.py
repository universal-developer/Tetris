import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
COLS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE


# --- constants ---
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

COLS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# --- game class ---


class Game:
    def __init__(self):
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()

    def draw_grid(self):
        # vertical lines
        for col in range(COLS + 1):
            pygame.draw.line(
                self.surface,
                BLACK,
                (col * CELL_SIZE, 0),
                (col * CELL_SIZE, GAME_HEIGHT),
                1
            )

        # horizontal lines
        for row in range(ROWS + 1):
            pygame.draw.line(
                self.surface,
                BLACK,
                (0, row * CELL_SIZE),
                (GAME_WIDTH, row * CELL_SIZE),
                1
            )

    def run(self):
        self.surface.fill(WHITE)
        self.draw_grid()
        self.display_surface.blit(self.surface, (0, 0))


# --- main loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption("Grid Example")

    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.run()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
