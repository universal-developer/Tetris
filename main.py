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

    def move_down(self,mouv):
        self.y += mouv

    def rotated_shape(self):
        if self.width >= 2 or self.height >= 2:
            return [(1 - cy, cx - 1) for cx, cy in self.shape]
        else:
            return self.shape

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
        self.mouvement = 1

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris – manual movement + lock test")

        self.clock = pygame.time.Clock()

        self.reset_game()

    def reset_game(self):
        #restart all the game
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.figure = Figure()
        self.running = True
        self.down = False
        self.game_over = False

        font = pygame.font.SysFont("arial", 30)
        self.button_text = font.render("Rejouer", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(self.width // 2, self.height // 2 + 60))

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

        #print "gamme over" + button "rejouer"
        if self.game_over:
            font = pygame.font.SysFont("arial", 40)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, rect)

            pygame.draw.rect(self.screen, (100, 100, 100), self.button_rect.inflate(40, 20))
            pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect.inflate(40, 20), 2)
            self.screen.blit(self.button_text, self.button_rect)

    def lock_figure(self):
        for cx, cy in self.figure.shape:
            px = self.figure.x + cx
            py = self.figure.y + cy
            if 0 <= px < self.cols and 0 <= py < self.rows:
                self.grid[py][px] = 1

        # New figure
        new_figure = Figure()
        self.down = False

        # if colision at the start = game over
        for cx, cy in new_figure.shape:
            px = new_figure.x + cx
            py = new_figure.y + cy
            if self.grid[py][px] == 1:
                self.game_over = True
                return

        self.figure = new_figure

    def can_move(self, dx, dy):
        for cx, cy in self.figure.shape:
            px = self.figure.x + cx + dx
            py = self.figure.y + cy + dy
            if px < 0 or px >= self.cols or py < 0 or py >= self.rows or self.grid[py][px] == 1:
                return False
        return True

    def clear_full_rows(self):
        new_grid = []
        lines_cleared = 0
        for row in self.grid:
            if any(cell == 0 for cell in row):
                new_grid.append(row)
            else:
                lines_cleared += 1

        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.cols)])

        self.grid = new_grid
        
    def inverse(self):
        self.mouvement= - self.mouvement
        
        if self.figure.y == 0:
            self.figure.y = 15
        else:
            self.figure.y = 0

    def run(self):
        fall_time = 0
        fall_speed = 300

        while self.running:
            dt = self.clock.tick(30)
            fall_time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # --- Clique sur le bouton "Rejouer" ---
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    if self.button_rect.inflate(40, 20).collidepoint(event.pos):
                        self.reset_game()  # redémarre le jeu

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        if self.down:
                            self.down = False

                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT and self.can_move(-1, 0):
                        self.figure.move_left()
                        
                    elif event.key == pygame.K_RIGHT and self.can_move(1, 0):
                        self.figure.move_right()
                        
                    elif event.key == pygame.K_DOWN:
                        self.down = True
                        
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
                            
                    elif event.key == pygame.K_l:
                        self.inverse()

            # auto fall
            if not self.game_over:
                if fall_time > fall_speed:
                    fall_time = 0
                    if self.can_move(0, self.mouvement):
                        self.figure.move_down(self.mouvement)
                    else:
                        self.lock_figure()
                        self.clear_full_rows()

                if self.down:
                    if self.can_move(0, self.mouvement):
                        self.figure.move_down(self.mouvement)
                    else:
                        self.lock_figure()
                        self.clear_full_rows()

            temp_grid = [row[:] for row in self.grid]
            if not self.game_over:
                self.figure.draw(temp_grid)

            self.draw_grid(temp_grid)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()

