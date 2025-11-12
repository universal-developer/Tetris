from base_tetris import BaseTetris, Figure
import pygame

class Game(BaseTetris):
    def __init__(self, rows=20, cols=10, cell_size=30):
        # Initialize the inverted Tetris with negative gravity
        super().__init__(rows, cols, cell_size, gravity=-1)
        pygame.display.set_caption("Tetris – Inversé")

        # Pause system variables
        self.paused = False
        self.pause_font = pygame.font.SysFont("arial", 40)
        self.button_font = pygame.font.SysFont("arial", 30)
        self.resume_rect = None
        self.quit_rect = None

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

    def toggle_pause(self):
        self.paused = not self.paused

    def draw_pause_menu(self):
        # Draw translucent background
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Title
        text = self.pause_font.render("PAUSE", True, (255, 255, 255))
        rect = text.get_rect(center=(self.width // 2, self.height // 2 - 80))
        self.screen.blit(text, rect)

        # Resume button
        resume_text = self.button_font.render("Reprendre", True, (255, 255, 255))
        self.resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2))
        pygame.draw.rect(self.screen, (100, 100, 100), self.resume_rect.inflate(80, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), self.resume_rect.inflate(80, 20), 2)
        self.screen.blit(resume_text, self.resume_rect)

        # Quit button
        quit_text = self.button_font.render("Quitter", True, (255, 255, 255))
        self.quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        pygame.draw.rect(self.screen, (100, 100, 100), self.quit_rect.inflate(80, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), self.quit_rect.inflate(80, 20), 2)
        self.screen.blit(quit_text, self.quit_rect)

    def run(self):
        # Main game loop
        fall_time = 0
        fall_speed = 300  # milliseconds between automatic downward moves

        while self.running:
            dt = self.clock.tick(30)
            fall_time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif self.paused:
                    # Pause menu interactions
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.resume_rect and self.resume_rect.inflate(30, 10).collidepoint(event.pos):
                            self.toggle_pause()
                        elif self.quit_rect and self.quit_rect.inflate(30, 10).collidepoint(event.pos):
                            # Return to menu
                            return

                # Restart after game over
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    if self.button_rect.inflate(40, 20).collidepoint(event.pos):
                        self.reset_game()

                elif event.type == pygame.KEYDOWN and not self.game_over:
                    # Toggle pause
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()

                    elif not self.paused:
                        # Move left
                        if event.key == pygame.K_LEFT and self.can_move(self.figure, -1, 0):
                            self.figure.move_left()

                        # Move right
                        elif event.key == pygame.K_RIGHT and self.can_move(self.figure, 1, 0):
                            self.figure.move_right()

                        # Move down manually
                        elif event.key == pygame.K_DOWN:
                            if self.can_move(self.figure, 0, self.gravity):
                                self.figure.move_down(self.gravity)
                            else:
                                self.lock_figure(self.figure)
                                self.clear_full_rows()

                        # Rotate piece
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

            # Handle pause freeze
            if self.paused:
                temp_grid = [row[:] for row in self.grid]
                self.figure.draw(temp_grid)
                self.draw_grid(temp_grid)
                self.draw_pause_menu()
                pygame.display.flip()
                continue

            # Automatic falling behavior
            if not self.game_over:
                if fall_time > fall_speed:
                    fall_time = 0
                    if self.can_move(self.figure, 0, self.gravity):
                        self.figure.move_down(self.gravity)
                    else:
                        self.lock_figure(self.figure)
                        self.clear_full_rows()

            # Draw frame
            temp_grid = [row[:] for row in self.grid]
            if not self.game_over:
                self.figure.draw(temp_grid)
            self.draw_grid(temp_grid)

            # Draw game over overlay
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

            self.draw_ui()
            pygame.display.flip()

        # Don’t quit pygame — return to main menu cleanly
        return
