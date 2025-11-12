import pygame
import random

# --- Define all Tetris shapes ---
SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],           # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],           # O
    [(0, 0), (1, 0), (2, 0), (2, 1)],           # L
    [(0, 0), (1, 0), (2, 0), (0, 1)],           # J
    [(0, 0), (1, 0), (2, 0), (1, 1)],           # T
    [(1, 0), (2, 0), (0, 1), (1, 1)],           # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],           # Z
]


class Figure:
    def __init__(self, start_y):
        self.shape = random.choice(SHAPES)
        self.width = max(self.shape, key=lambda x: x[0])[0]
        self.height = max(self.shape, key=lambda x: x[1])[1]
        self.x = 3
        self.y = start_y

    def draw(self, board, value=1):
        for cx, cy in self.shape:
            px = self.x + cx
            py = self.y + cy
            if 0 <= px < len(board[0]) and 0 <= py < len(board):
                board[py][px] = value

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self, mouv=1):
        self.y += mouv

    def rotated_shape(self):
        # exact same rotation logic as before
        return [(-cy + 1, cx) for cx, cy in self.shape]

    def apply_rotation(self, new_shape):
        self.shape = new_shape
        self.width, self.height = self.height, self.width


class BaseTetris:
    def __init__(self, rows=20, cols=10, cell_size=30, gravity=1):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80
        self.gravity = gravity
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.score = 0  # 🟢 new line

    def draw_grid(self, grid):
        # 🟢 Clear the entire screen first
        self.screen.fill((0, 0, 0))

        # Draw cells
        for r in range(self.rows):
            for c in range(self.cols):
                val = grid[r][c]
                color = (255, 255, 255) if val else (0, 0, 0)
                rect = pygame.Rect(
                    c * self.cell_size + 20,
                    r * self.cell_size + 60,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        # 🟢 Draw the score freshly each frame
        font = pygame.font.SysFont("arial", 24)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))



    def can_move(self, figure, dx, dy):
        for cx, cy in figure.shape:
            px = figure.x + cx + dx
            py = figure.y + cy + dy
            if px < 0 or px >= self.cols or py < 0 or py >= self.rows or self.grid[py][px] == 1:
                return False
        return True

    def lock_figure(self, figure):
        for cx, cy in figure.shape:
            px = figure.x + cx
            py = figure.y + cy
            if 0 <= px < self.cols and 0 <= py < self.rows:
                self.grid[py][px] = 1

        # spawn new piece after locking
        start_y = 0 if self.gravity == 1 else 18
        self.figure = Figure(start_y)
