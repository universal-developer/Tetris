import pygame
import random

# --- Shapes ---
shapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],           # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],           # O
    [(0, 0), (1, 0), (2, 0), (2, 1)],           # L
    [(0, 0), (1, 0), (2, 0), (0, 1)],           # J
    [(0, 0), (1, 0), (2, 0), (1, 1)],           # T
    [(1, 0), (2, 0), (0, 1), (1, 1)],           # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],           # Z
]


# --- Figure class ---
class Figure:
    def __init__(self):
        self.pos_x = 3        # start roughly in middle
        self.pos_y = 0
        self.shape = random.choice(shapes)

    def draw(self, board, value=1):
        """Draw or erase the figure on the board."""
        for cx, cy in self.shape:
            x = self.pos_x + cx
            y = self.pos_y + cy
            if 0 <= x < len(board[0]) and 0 <= y < len(board):
                board[y][x] = value

    def down(self):
        self.pos_y += 1

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1

    def right(self, cols):
        if self.pos_x < cols - 4:  # prevent going off grid
            self.pos_x += 1


# --- Game class ---
class Game:
    def __init__(self, rows=20, cols=10, cell_size=30):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris grid")

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.figure = Figure()
        self.running = True

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                color = (255, 255, 255) if value == 1 else (0, 0, 0)
                rect = pygame.Rect(
                    c * self.cell_size + 20,
                    r * self.cell_size + 60,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            # --- handle events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.figure.left()
                    elif event.key == pygame.K_RIGHT:
                        self.figure.right(self.cols)
                    elif event.key == pygame.K_DOWN:
                        self.figure.down()

            # --- clear and redraw ---
            self.grid = [[0 for _ in range(self.cols)]
                         for _ in range(self.rows)]
            self.figure.draw(self.grid, value=1)

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


# --- main ---
if __name__ == "__main__":
    Game().run()
