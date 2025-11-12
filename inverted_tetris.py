from base_tetris import BaseTetris, Figure
import pygame

class Game(BaseTetris):
    def __init__(self, rows=20, cols=10, cell_size=30):
        # Initialize the inverted Tetris with negative gravity
        super().__init__(rows, cols, cell_size, gravity=-1)
        pygame.display.set_caption("Tetris – Inversé")

    def clear_full_rows(self):
        # Removes all full rows from the grid and increases the score
        new_grid = []
        lines_cleared = 0

        # Keep rows that are not full, count those that are
        for row in self.grid:
            if any(cell == 0 for cell in row):
                new_grid.append(row)
            else:
                lines_cleared += 1

        # Add empty rows at the top for every cleared line
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.cols)])

        # Update the grid and score
        self.grid = new_grid
        self.score += lines_cleared * 100

    def run(self):
        # Main game loop
        fall_time = 0
        fall_speed = 300  # milliseconds between automatic downward moves

        while self.running:
            dt = self.clock.tick(30)  # keeps the game running at ~30 FPS
            fall_time += dt

            # Handle all player and system events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Restart the game if "Rejouer" is clicked after game over
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    if self.button_rect.inflate(40, 20).collidepoint(event.pos):
                        self.reset_game()

                # Handle keyboard input while game is active
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    # Move piece left if possible
                    if event.key == pygame.K_LEFT and self.can_move(self.figure, -1, 0):
                        self.figure.move_left()

                    # Move piece right if possible
                    elif event.key == pygame.K_RIGHT and self.can_move(self.figure, 1, 0):
                        self.figure.move_right()

                    # Move piece down manually
                    elif event.key == pygame.K_DOWN:
                        if self.can_move(self.figure, 0, self.gravity):
                            self.figure.move_down(self.gravity)
                        else:
                            self.lock_figure(self.figure)
                            self.clear_full_rows()

                    # Rotate piece clockwise if space available
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

            # Automatic falling behavior
            if not self.game_over:
                if fall_time > fall_speed:
                    fall_time = 0
                    # If the piece can move down, move it
                    if self.can_move(self.figure, 0, self.gravity):
                        self.figure.move_down(self.gravity)
                    # Otherwise, lock it in place and check for completed rows
                    else:
                        self.lock_figure(self.figure)
                        self.clear_full_rows()

            # Copy grid to draw both locked and falling pieces
            temp_grid = [row[:] for row in self.grid]
            if not self.game_over:
                self.figure.draw(temp_grid)

            # Draw current frame (grid, pieces, score)
            self.draw_grid(temp_grid)

            # Draw the "Game Over" overlay and button
            if self.game_over:
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))

                text = self.font.render("GAME OVER", True, (255, 0, 0))
                rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(text, rect)

                pygame.draw.rect(self.screen, (100, 100, 100), self.button_rect.inflate(40, 20))
                pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect.inflate(40, 20), 2)
                self.screen.blit(self.button_text, self.button_rect)

            pygame.display.flip()

        pygame.quit()
