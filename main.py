import pygame
import random

# --- Define all Tetris shapes ---
shapes = [
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
        self.shape = random.choice(shapes)
        self.pos_x = 3
        self.pos_y = 0

    def draw(self, board, value=1):
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

    def draw_grid(self):
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
                
    def draw_grid_overlay(self, grid):
        for r in range(self.rows):
            for c in range(self.cols):
                value = grid[r][c]
                color = (255, 255, 255) if value else (0, 0, 0)
                rect = pygame.Rect(c * self.cell_size + 20, r * self.cell_size + 60, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)


    def lock_figure(self):
        for cx, cy in self.figure.shape: 
            # Convert local block coordinates (cx, cy) into global board coordinates
            # by adding the figure's current position offset.
            x = self.figure.pos_x + cx 
            y = self.figure.pos_y + cy
            
            if 0 <= x < self.cols and 0 <= y < self.rows: # Check whether the figure is actually within the matrix
                self.grid[y][x] = 1
                
        self.figure = Figure() # Spawn a new figure
            

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Make sure the figure doesn't leave the grid
                        can_move = True
                        for cx, cy in self.figure.shape:
                            x = self.figure.pos_x + cx - 1 # First col of the grid
                            y = self.figure.pos_y + cy
                            if x < 0 or self.grid[y][x] == 1:
                                can_move = False
                                break
                        if can_move:
                            self.figure.left()

                    elif event.key == pygame.K_RIGHT:
                        # Make sure the figure doesn't leave the grid
                        can_move = True
                        for cx, cy in self.figure.shape:
                            x = self.figure.pos_x + cx + 1 # Last col of the grid
                            y = self.figure.pos_y + cy
                            if x >= self.cols or self.grid[y][x] == 1:
                                can_move = False
                                break
                        if can_move:
                            self.figure.right()

                    elif event.key == pygame.K_DOWN:
                        
                        # Collision implimented
                        self.figure.pos_y += 1
                        
                        collision = False
                        
                        for cx, cy in self.figure.shape:
                            x = self.figure.pos_x + cx
                            y = self.figure.pos_y + cy
                            
                            if y >= self.rows: # check whether we have reached the bottom of the grid
                                collission = True
                                break
                            
                            if y + 1 >= self.rows or (y + 1 < self.rows and self.grid[y + 1][x] == 1): # compare to 
                                collision = True
                                break
                            
                        if collision: 
                            self.lock_figure() 
        
            temp_grid = [row[:] for row in self.grid]
            self.figure.draw(temp_grid)                # draw active figure on top

            #self.screen.fill((0, 0, 0))
            self.draw_grid_overlay(temp_grid)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
