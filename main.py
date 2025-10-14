import pygame


class Game:
    def __init__(self, rows=10, cols=10, cell_size=40):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size

        # set up window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid of 0 and 1")

        # generate checkerboard grid
        self.grid = [[0 for r in range(rows)] for c in range(cols)]
        print(self.grid)

        self.running = True

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c * self.cell_size, r *
                                   self.cell_size, self.cell_size, self.cell_size)

                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

    def run(self):
        """Main loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
