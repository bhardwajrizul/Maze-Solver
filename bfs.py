import pygame
from collections import deque
import random 

# Define constants
WIDTH = 600
ROWS = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_traversed(self):
        self.color = DARK_BLUE

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check the node below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Check the node above
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Check the node to the right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Check the node to the left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def bfs(win, start, end, grid):
    queue = deque([start])
    came_from = {start: None}
    visited_nodes = []

    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path, visited_nodes

        for neighbor in current.neighbors:
            if neighbor not in came_from:
                came_from[neighbor] = current
                neighbor.make_traversed()
                visited_nodes.append(neighbor)
                queue.append(neighbor)
        draw(win, grid)
        pygame.time.delay(50)
    return [], visited_nodes

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, ROWS, WIDTH)
    pygame.display.update()

def generate_maze(grid, rows):
    for _ in range(rows*rows // 4):  # Fills roughly 25% of the grid with barriers
        x = random.randint(0, rows - 1)
        y = random.randint(0, rows - 1)
        grid[x][y].make_barrier()

    start_x = random.randint(0, rows - 1)
    start_y = random.randint(0, rows - 1)
    grid[start_x][start_y].make_start()

    end_x = random.randint(0, rows - 1)
    end_y = random.randint(0, rows - 1)
    while end_x == start_x and end_y == start_y:
        end_x = random.randint(0, rows - 1)
        end_y = random.randint(0, rows - 1)
    grid[end_x][end_y].make_end()

    return grid[start_x][start_y], grid[end_x][end_y]

def reset_grid(grid):
    for row in grid:
        for node in row:
            node.reset()

def main(win, width):
    grid = make_grid(ROWS, width)
    start, end = generate_maze(grid, ROWS)
    run = True

    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_grid(grid)
                    start, end = generate_maze(grid, ROWS)

                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    bfs_path, visited_nodes = bfs(win, start, end, grid)
                    for node in visited_nodes:
                        if node not in bfs_path and node.color != GREEN and node.color != RED:
                            node.color = LIGHT_BLUE
                    for node in bfs_path:
                        node.make_path()
                        draw(win, grid)
                        pygame.time.delay(100)
                    start.make_start()
                    end.make_end()

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("BFS Maze Solver")
    main(WIN, WIDTH)