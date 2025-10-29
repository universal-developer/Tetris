import pygame
import random

# --- Define all Tetris shapes ---
# Each shape = 4 (x, y) coordinates relative to its own top-left corner
shapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],           # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],           # O
    [(0, 0), (1, 0), (2, 0), (2, 1)],           # L
    [(0, 0), (1, 0), (2, 0), (0, 1)],           # J
    [(0, 0), (1, 0), (2, 0), (1, 1)],           # T
    [(1, 0), (2, 0), (0, 1), (1, 1)],           # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],           # Z
]

# --- Figure class: one active piece ---


class Figure:
    def __init__(self):
        self.shape = random.choice(shapes)  # choose one of the shapes
        self.pos_x = 3  # column on the main grid
        self.pos_y = 0  # row on the main grid

    def draw(self, board, value=1):
        """Mark cells on the board (value = 1 means filled)."""
        for cx, cy in self.shape:
            x = self.pos_x + cx
            y = self.pos_y + cy
            if 0 <= x < len(board[0]) and 0 <= y < len(board):
                board[y][x] = value

    def left(self):
        self.pos_x -= 1

    def right(self):
        self.pos_x += 1

    def down(self):
        self.pos_y += 1


# --- Game class: board + controls + drawing ---


class Game:
    def __init__(self, rows=20, cols=10, cell_size=30):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris – manual movement only")

        # Create an empty grid (2D list)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.figure = Figure()
        self.running = True

    def draw_grid(self):
        """Draws cells of the grid."""
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                color = (255, 255, 255) if value else (0, 0, 0)
                rect = pygame.Rect(
                    c * self.cell_size + 20,
                    r * self.cell_size + 60,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            # --- Handle inputs ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.figure.left()
                    elif event.key == pygame.K_RIGHT:
                        self.figure.right()
                    elif event.key == pygame.K_DOWN:
                        self.figure.down()

            # --- Clear grid and draw current piece ---
            self.grid = [[0 for _ in range(self.cols)]
                         for _ in range(self.rows)]
            self.figure.draw(self.grid)

            # --- Render everything ---
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()

            clock.tick(30)

        pygame.quit()


# --- Run the game ---
if __name__ == "__main__":
    Game().run()
