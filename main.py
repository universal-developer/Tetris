import pygame
import random

# --- Shapes: defined by local (x, y) tile coordinates ---
# Each shape is a list of 4 tuples relative to its own top-left corner
shapes = [
    [(0, 1), (1, 1), (2, 1), (3, 1)],           # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],           # O
    [(0, 0), (1, 0), (2, 0), (2, 1)],           # L
    [(0, 0), (1, 0), (2, 0), (0, 1)],           # J
    [(0, 0), (1, 0), (2, 0), (1, 1)],           # T
    [(1, 0), (2, 0), (0, 1), (1, 1)],           # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],           # Z
]

# --- Figure class: represents a single falling Tetris piece ---


class Figure:
    def __init__(self):
        self.pos_x = 3        # start near the middle of the grid
        self.pos_y = 0        # start at top row
        self.shape = random.choice(shapes)  # randomly pick one of the 7 shapes
        self.largeur=max(self.shape, key=lambda x: x[0])[0]
        self.longueur=max(self.shape, key=lambda x: x[1])[1]

    def draw(self, board, value=1):
        """Draw (value=1) or erase (value=0) the figure on the main grid."""
        for cx, cy in self.shape:
            # Convert local shape coordinates -> global board coordinates
            x = self.pos_x + cx
            y = self.pos_y + cy

            # print(x, y)  # debug: print coordinates of each tile
            # Only draw inside valid grid boundaries
            if 0 <= x < len(board[0]) and 0 <= y < len(board):
                board[y][x] = value  # mark cell as filled (1) or empty (0)

    # --- Movement controls ---
    def rotate(self, board):
        # Create the rotated shape
        new_shape = [(largeur-cy+, cx) for cx, cy in self.shape]  
        self.shape = new_shape
        self.longueur, self.largeur= self.largeur, self.longueur
        
    def down(self):
        self.pos_y += 1  # move shape one row down

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1  # move one column left (if not at wall)

    def right(self, cols):
        if self.pos_x < cols - self.largeur -1:  # quick bound check, prevents going off right side
            self.pos_x += 1


# --- Game class: handles the grid, input, and rendering ---
class Game:
    def __init__(self, rows=20, cols=10, cell_size=30):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80

        self.fall_time = 0
        self.fall_speed = 500  # milliseconds per step

        # Pygame window setup
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris grid")

        # 2D list representing the game board (0 = empty, 1 = filled)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.figure = Figure()  # create the first random piece
        self.running = True

    def draw_grid(self):
        """Draws the board on the screen based on current grid values."""
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                color = (255, 255, 255) if value == 1 else (0, 0, 0)
                rect = pygame.Rect(
                    c * self.cell_size + 20,   # X pixel offset
                    r * self.cell_size + 60,   # Y pixel offset
                    self.cell_size,            # width & height of one cell
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                # draw light-gray border for grid visibility
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def gravity(self):
        self.move_y += 3.2
        pass

    def collision(self, shape, pos_x, pos_y):
        for cx, cy in shape:
            x = pos_x + cx
            y = pos_y + cy

            if y >= self.rows or self.grid[y][x] == 1:
                return True

    def lock_piece(self):
        """When a piece lands, mark its tiles as filled in the grid."""
        for cx, cy in self.figure.shape:
            x = self.figure.pos_x + cx
            y = self.figure.pos_y + cy
            if 0 <= x < self.cols and 0 <= y < self.rows:
                self.grid[y][x] = 1

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            # --- Input handling ---
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
                    elif event.key == pygame.K_UP:
                        self.figure.rotate(self.grid)

            # --- Gravity logic ---
            self.fall_time += clock.get_time()
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                if not self.collision(self.figure.shape, self.figure.pos_x, self.figure.pos_y + 1):
                    self.figure.pos_y += 1
                else:
                    self.lock_piece()
                    self.figure = Figure()

            # --- Clear + redraw grid each frame ---
            self.grid = [[0 for _ in range(self.cols)]
                         for _ in range(self.rows)]
            self.figure.draw(self.grid, value=1)

            # --- Drawing ---
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()

            # --- Limit FPS ---
            clock.tick(30)

        pygame.quit()


# --- Run the game ---
if __name__ == "__main__":
    Game().run()
