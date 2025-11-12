from base_tetris import BaseTetris, Figure
import pygame

class Game(BaseTetris):
    def __init__(self, rows=20, cols=10, cell_size=30):
        super().__init__(rows, cols, cell_size, gravity=-1)
        pygame.display.set_caption("Tetris – Inversé")
        self.mouvement = -1
        self.figure = Figure(start_y=18)
        self.down = False
        self.game_over = False
        self.font = pygame.font.SysFont("arial", 30)
        self.button_text = self.font.render("Rejouer", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(self.width // 2, self.height // 2 + 60))


    def clear_full_rows(self):
        new_grid = []
        lines_cleared = 0
        for row in self.grid[::self.mouvement]:
            if any(cell == 0 for cell in row):
                pos_insert=int(-0.5-self.mouvement*0.5)
                new_grid.insert(pos_insert,row)
            else:
                lines_cleared += 1

        for _ in range(lines_cleared):
            new_grid.insert(self.mouvement, [0 for _ in range(self.cols)])

        self.grid = new_grid
        
        self.score += lines_cleared * 100
        print("Score:", self.score)



    def inverse(self):
        self.mouvement = -self.mouvement
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
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT and self.can_move(self.figure, -1, 0):
                        self.figure.move_left()
                    elif event.key == pygame.K_RIGHT and self.can_move(self.figure, 1, 0):
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
                elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    self.down = False

            if not self.game_over:
                if fall_time > fall_speed:
                    fall_time = 0
                    if self.can_move(self.figure, 0, self.mouvement):
                        self.figure.move_down(self.mouvement)
                    else:
                        self.lock_figure(self.figure)
                        self.clear_full_rows()
                if self.down:
                    if self.can_move(self.figure, 0, self.mouvement):
                        self.figure.move_down(self.mouvement)
                    else:
                        self.lock_figure(self.figure)
                        self.clear_full_rows()

            temp_grid = [row[:] for row in self.grid]
            if not self.game_over:
                self.figure.draw(temp_grid)
            self.draw_grid(temp_grid)
            pygame.display.flip()

        pygame.quit()
