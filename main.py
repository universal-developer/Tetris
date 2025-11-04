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
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.width = max(self.shape, key=lambda x: x[0])[0]
        self.height = max(self.shape, key=lambda x: x[1])[1]
        self.x = 3
        self.y = 0

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

    def move_down(self):
        self.y += 1

    def rotated_shape(self):
        # Generate a new rotated version of the shape (90° clockwise)
        return [(-cy + 1, cx) for cx, cy in self.shape]

    def apply_rotation(self, new_shape):
        self.shape = new_shape
        self.width, self.height = self.height, self.width


class Game:
    def __init__(self, rows=20, cols=10, cell_size=30):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris – manual movement + lock test")

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.figure = Figure()
        self.running = True

    def draw_grid(self, grid):
        for r in range(self.rows):
            for c in range(self.cols):
                value = grid[r][c]
                color = (255, 255, 255) if value else (0, 0, 0)
                rect = pygame.Rect(
                    c * self.cell_size + 20,
                    r * self.cell_size + 60,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def lock_figure(self):
        for cx, cy in self.figure.shape:
            px = self.figure.x + cx
            py = self.figure.y + cy
            if 0 <= px < self.cols and 0 <= py < self.rows:
                self.grid[py][px] = 1
        self.figure = Figure()

    def can_move(self, dx, dy):
        for cx, cy in self.figure.shape:
            px = self.figure.x + cx + dx
            py = self.figure.y + cy + dy
            if px < 0 or px >= self.cols or py < 0 or py >= self.rows or self.grid[py][px] == 1:
                return False
        return True

    def run(self):
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 300  # milliseconds per step
        down=False

        while self.running:
            dt = clock.tick(30)
            fall_time += dt

            if down == True:
                # Try moving down
                if self.can_move(0, 1):
                    self.figure.move_down()
                else:
                    # can't move down → lock piece
                    self.lock_figure()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYUP :
                    if down == True:
                        down = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.can_move(-1, 0):
                        self.figure.move_left()
                        
                    elif event.key == pygame.K_RIGHT and self.can_move(1, 0):
                        self.figure.move_right()
                        
                    elif event.key == pygame.K_DOWN:
                         down = True
                        
                    elif event.key == pygame.K_UP:
                        new_shape = self.figure.rotated_shape()
                        can_rotate = True
                        for cx, cy in new_shape:
                            px = self.figure.x + cx
                            py = self.figure.y + cy
                            if px < 0 or px >= self.cols or py < 0 or py >= self.rows or self.grid[py][px] == 1:
                                can_rotate = False
                                break
                        if can_rotate:
                            self.figure.apply_rotation(new_shape)

            if fall_time > fall_speed:
                fall_time = 0
                if self.can_move(0, 1):
                    self.figure.move_down()
                elif not self.can_move(0, 1):
                    self.lock_figure()

            temp_grid = [row[:] for row in self.grid]
            self.figure.draw(temp_grid)
            self.draw_grid(temp_grid)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()
