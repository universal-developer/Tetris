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

SHAPES2 = [
    [(0, 0), (1, 0), (2, 0), (3, 0)]           # Z
]

######################class objet########################################

class Figure: 
    def __init__(self):
        self.shape = random.choice(SHAPES) #choisi une forme au hasard
        self.width = max(self.shape, key=lambda x: x[0])[0] #longueur de la forme
        self.height = max(self.shape, key=lambda x: x[1])[1] #hauteur de la forme
        self.x = 3 #position de depart en x
        self.y = 0 #position de depart en y

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
        if self.width >= 2 or self.height >=2:
            return [(1-cy, cx-1) for cx, cy in self.shape ]
        else:
            return self.shape
        

    def apply_rotation(self, new_shape):
        self.shape = new_shape
        self.width, self.height = self.height, self.width

############################# fonction ######################################

def draw_grid(grid): #redecine la grille de jeu a chaque etape
    for r in range(rows):
        for c in range(cols):
            value = grid[r][c]
            color = (255, 255, 255) if value else (0, 0, 0)
            rect = pygame.Rect(
                c * cell_size + 20,
                r * cell_size + 60,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)


def lock_figure(): #rend la figure immobile + crée une nouvelle figure
    global figure,down
    for cx, cy in figure.shape:
        px = figure.x + cx
        py = figure.y + cy
        if 0 <= px < cols and 0 <= py < rows:
            grid[py][px] = 1
    down=False
    figure = Figure()


def can_move( dx, dy): #test si la figure peux ce deplacer une position
    for cx, cy in figure.shape:
        px = figure.x + cx + dx
        py = figure.y + cy + dy
        if px < 0 or px >= cols or py < 0 or py >= rows or grid[py][px] == 1:
            return False
    return True
    

def clear_full_rows():
    global grid
    new_grid = []
    lines_cleared = 0
        
    for row in grid:
        if any(cell == 0 for cell in row):
            new_grid.append(row)
        else: 
            lines_cleared += 1
                
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in range(cols)])

    grid = new_grid


def run():
    global running, down
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 300  # milliseconds per step

    while running:
        dt = clock.tick(30)
        fall_time += dt
        
        if down == True:
            # Try moving down
            if can_move(0, 1):
                figure.move_down()
            else:
                # can't move down → lock piece
                lock_figure()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYUP :
                if down == True:
                    down = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and can_move(-1, 0):
                    figure.move_left()
                    
                elif event.key == pygame.K_RIGHT and can_move(1, 0):
                    figure.move_right()
                    
                elif event.key == pygame.K_DOWN:
                    down = True
                        
                elif event.key == pygame.K_UP:
                    new_shape = figure.rotated_shape()
                    can_rotate = True
                    for cx, cy in new_shape:
                        px = figure.x + cx
                        py = figure.y + cy
                        if px < 0 or px >= cols or py < 0 or py >= rows or grid[py][px] == 1:
                            can_rotate = False
                            break
                    if can_rotate:
                        figure.apply_rotation(new_shape)

        if fall_time > fall_speed:
            fall_time = 0
            if can_move(0, 1):
                #figure.move_down()
                None
            else:
                lock_figure()
                clear_full_rows()

        temp_grid = [row[:] for row in grid]
        figure.draw(temp_grid)
        draw_grid(temp_grid)
        pygame.display.flip()

    pygame.quit()

############################# main code #####################################



pygame.init()
rows = 20
cols = 10
cell_size = 30
width = cols * cell_size + 40
height = rows * cell_size + 80

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris – manual movement + lock test")

grid = [[0 for _ in range(cols)] for _ in range(rows)]
figure = Figure()
running = True
down=False







if __name__ == "__main__":
    run()
