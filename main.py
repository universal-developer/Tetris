import pygame


forme_possible=[["forme1"],["forme2"],["forme3"]]

class Forme:
    def __init__(self):
        self.pos_x = 5
        self.pos_y = 0
        self.forme=random.choice(forme_possible)
        
    def decendre(self):
        self.pos_y+=1
    
    def gauche(self):
        if self.pos_x>0:
            self.pos_x-=1
    
    def droit(self):
        if self.pos_x<10:
            self.pos_x+=1

class Game:
    def __init__(self, rows=20, cols=10, cell_size=30):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 40
        self.height = rows * cell_size + 80

        # set up window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid of 0 and 1")

        # generate checkerboard grid
        self.grid = [[0 for c in range(cols)] for r in range(rows)]
        print(self.grid)

        self.running = True

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                color = (255, 255, 255) if value == 1 else (0, 0, 0)
                rect = pygame.Rect(c * self.cell_size + 20, r *
                                   self.cell_size + 60, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200),
                                 rect, 1)  # light gray outline

    def run(self):
        """Main loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.Forme.gauche()
                if event.key == pygame.K_RIGHT:
                    self.Forme.droit

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
