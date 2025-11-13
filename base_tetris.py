import pygame
import random

# --- Define all Tetris shapes ---
SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(0, 0), (1, 0), (2, 0), (2, 1)],  # L
    [(0, 0), (1, 0), (2, 0), (0, 1)],  # J
    [(0, 0), (1, 0), (2, 0), (1, 1)],  # T
    [(1, 0), (2, 0), (0, 1), (1, 1)],  # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
]


class Figure:
    def __init__(self, start_y, cols=10):
        self.shape = random.choice(SHAPES)
        self.width = max(self.shape, key=lambda x: x[0])[0]
        self.height = max(self.shape, key=lambda x: x[1])[1]
        self.x = (cols - (self.width + 1)) // 2  # Dynamically centered
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
        self.gravity = gravity

        # unified top bar space
        self.top_margin = 56
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80 + self.top_margin

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.reset_game()

        self.piece_queue = []
        for _ in range(3):
            self.piece_queue.append(Figure(start_y=0 if gravity == 1 else 18, cols=cols))


    def draw_grid(self, grid):
        """Draw playfield + top info bar."""
        self.screen.fill((0, 0, 0))

        # Continuous dark top bar for both score and controls
        pygame.draw.rect(self.screen, (25, 25, 25), (0, 0, self.width, self.top_margin))
        pygame.draw.line(
            self.screen, (80, 80, 80), (0, self.top_margin), (self.width, self.top_margin), 1
        )

        # Draw playfield grid
        for r in range(self.rows):
            for c in range(self.cols):
                val = grid[r][c]
                color = (255, 255, 255) if val else (0, 0, 0)
                rect = pygame.Rect(
                    c * self.cell_size + 20,
                    r * self.cell_size + 60 + self.top_margin,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        # Draw top bar info
        self.draw_ui()

    def draw_ui(self):
        """Score on the left; controls on the right.
        Auto-wrap controls to a second line if there's not enough room.
        Ensures no overlap with the score."""
        font_bold = pygame.font.SysFont("arial", 24, bold=True)
        font_small = pygame.font.SysFont("arial", 18)

        # --- Score (left) ---
        score_surf = font_bold.render(f"Score: {self.score}", True, (255, 255, 255))
        score_pos = (20, 12)
        self.screen.blit(score_surf, score_pos)
        score_right = score_pos[0] + score_surf.get_width()

        # --- Controls text (right) ---
        controls_1line = "←/→ Déplacer   ↓ Descendre   ↑ Tourner   ÉCH Pause"
        w_1, h_1 = font_small.size(controls_1line)

        controls_2lines = [
            "←/→ Déplacer   ↓ Descendre",
            "↑ Tourner   ÉCH Pause",
        ]
        w_2 = max(
            font_small.size(controls_2lines[0])[0],
            font_small.size(controls_2lines[1])[0],
        )
        h_2_total = font_small.get_height() * 2 + 4

        left_limit = score_right + 30
        right_padding = 20
        available_width = self.width - right_padding - left_limit

        if w_1 <= available_width:
            # One-line layout
            x = self.width - right_padding - w_1
            if x < left_limit:
                x = left_limit
            self.screen.blit(
                font_small.render(controls_1line, True, (255, 255, 255)),
                (x, 16),
            )
        else:
            # Two-line layout (stacked neatly)
            x = self.width - right_padding - w_2
            if x < left_limit:
                x = left_limit
            y_top = 8
            self.screen.blit(
                font_small.render(controls_2lines[0], True, (255, 255, 255)),
                (x, y_top),
            )
            self.screen.blit(
                font_small.render(controls_2lines[1], True, (255, 255, 255)),
                (x, y_top + font_small.get_height() + 4),
            )

    def can_move(self, figure, dx, dy):
        for cx, cy in figure.shape:
            px = figure.x + cx + dx
            py = figure.y + cy + dy
            if (
                px < 0
                or px >= self.cols
                or py < 0
                or py >= self.rows
                or self.grid[py][px] == 1
            ):
                return False
        return True

    def lock_figure(self, figure):
        # Lock the current figure into the grid
        for cx, cy in figure.shape:
            px = figure.x + cx
            py = figure.y + cy
            if 0 <= px < self.cols and 0 <= py < self.rows:
                self.grid[py][px] = 1

        # Get the next figure from FIFO
        next_figure = self.get_next_figure()

        # Check collision for game over
        for cx, cy in next_figure.shape:
            px = next_figure.x + cx
            py = next_figure.y + cy
            if self.grid[py][px] == 1:
                self.game_over = True
                return

        # Set the next figure
        self.figure = next_figure

    def reset_game(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # reset file FIFO BEFORE spawning
        self.piece_queue = []
        for _ in range(3):
            self.piece_queue.append(Figure(start_y=0 if self.gravity == 1 else 18, cols=self.cols))

        # now take the first piece from the fresh queue
        self.figure = self.get_next_figure()

        self.score = 0
        self.down = False
        self.game_over = False

        self.font = pygame.font.SysFont("arial", 30)
        self.button_text = self.font.render("Rejouer", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(
            center=(self.width // 2, self.height // 2 + 60)
        )



    def get_next_figure(self):
        # FIFO → remove from front
        next_figure = self.piece_queue[0]
        del self.piece_queue[0]

        # Generate a new figure and add to the end
        start_y = 0 if self.gravity == 1 else 18
        new_piece = Figure(start_y, cols=self.cols)

        # Prevent 3 identical shapes
        if len(self.piece_queue) >= 2:
            if (self.piece_queue[-1].shape == new_piece.shape and
                self.piece_queue[-2].shape == new_piece.shape):
                # Force a new different one
                while new_piece.shape == self.piece_queue[-1].shape:
                    new_piece = Figure(start_y, cols=self.cols)

        self.piece_queue.append(new_piece)

        return next_figure

