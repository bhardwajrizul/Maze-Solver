import pygame
import random

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 150)
LIGHT_BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_traversed(self):
        self.color = DARK_BLUE

    def make_open(self):
        self.color = LIGHT_BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.row * CELL_SIZE, self.col * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def dfs(WIN, start, end, grid, running):
    stack = [start]
    visited = set()
    came_from = {start: None}
    while stack and running:
        current = stack.pop()
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path

        if current not in visited:
            visited.add(current)
            current.make_traversed()  # Mark the node as traversed immediately after visiting
            for neighbor in current.neighbors:
                if neighbor not in visited and neighbor not in stack:
                    came_from[neighbor] = current
                    stack.append(neighbor)
        else:
            current.color = LIGHT_BLUE
        draw(WIN, grid, ROWS, COLS)
        pygame.time.delay(50)
    return []



def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(Node(i, j))
    return grid

def draw_grid(win, rows, cols):
    for i in range(rows):
        pygame.draw.line(win, BLACK, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT))
    for j in range(cols):
        pygame.draw.line(win, BLACK, (0, CELL_SIZE * j), (WIDTH, CELL_SIZE * j))

def draw(win, grid, rows, cols):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, cols)
    pygame.display.update()

def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer (DFS)")
    grid = make_grid(ROWS, COLS)
    start = grid[0][0]
    end = grid[ROWS - 1][COLS - 1]
    while start == end:
        end = random.choice(random.choice(grid))
    start.make_start()
    end.make_end()
    for row in grid:
        for node in row:
            if random.randint(0, 3) == 0 and node != start and node != end:
                node.make_barrier()
    run = True
    while run:
        draw(WIN, grid, ROWS, COLS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
                node = grid[row][col]
                if event.button == 1:
                    if node.color == WHITE:
                        start.reset()
                        start = node
                        start.make_start()
                    elif node.color == RED:
                        start.reset()
                        start = None
                elif event.button == 3:
                    if node.color == GREEN:
                        end.reset()
                        end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and run:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    if run:
                        dfs_path = dfs(WIN, start, end, grid, run)
                    for node in dfs_path:
                        pygame.time.delay(50)
                        node.color = YELLOW
                        draw(WIN, grid, ROWS, COLS)
                    start.make_start()
                    end.make_end()
                elif event.key == pygame.K_ESCAPE:
                    start, end = None, None
                    grid = make_grid(ROWS, COLS)
                    start = grid[0][0]
                    end = grid[ROWS - 1][COLS - 1]
                    while start == end:
                        end = random.choice(random.choice(grid))
                    start.make_start()
                    end.make_end()
                    for row in grid:
                        for node in row:
                            if random.randint(0, 3) == 0 and node != start and node != end:
                                node.make_barrier()
                elif not run:
                    break
    pygame.quit()

if __name__ == "__main__":
    main()
