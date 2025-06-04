import pygame
import heapq

# 화면 설정
WIDTH = 600
ROWS = 30
CELL_SIZE = WIDTH // ROWS
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Multi-Path A* Visualization")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
PATH_COLORS = [(0, 0, 255), (0, 100, 200), (100, 0, 255), (255, 100, 0), (0, 200, 100)]

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g = float('inf')
        self.f = float('inf')
        self.prev = None

    def get_pos(self):
        return self.row, self.col

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE
        self.g = float('inf')
        self.f = float('inf')
        self.prev = None

    def make_obstacle(self): self.color = BLACK
    def make_start(self): self.color = GREEN
    def make_end(self): self.color = RED
    def draw(self): pygame.draw.rect(WIN, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
    def update_neighbors(self, grid):
        self.neighbors = []
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = self.row + d[0], self.col + d[1]
            if 0 <= r < ROWS and 0 <= c < ROWS and not grid[r][c].is_obstacle():
                self.neighbors.append(grid[r][c])
    def __lt__(self, other): return False

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def make_grid():
    return [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]

def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(WIN, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

def draw_all(grid):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    draw_grid()
    pygame.display.update()

def get_clicked_pos(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE  # row, col

def a_star_path(grid, start, end, avoid_set):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g, start.f = 0, heuristic(start, end)
    visited = {start}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current.prev:
                path.append(current)
                current = current.prev
            return path[::-1]
        for neighbor in current.neighbors:
            if neighbor in avoid_set:
                continue
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.f = temp_g + heuristic(neighbor, end)
                neighbor.prev = current
                if neighbor not in visited:
                    heapq.heappush(open_set, (neighbor.f, neighbor))
                    visited.add(neighbor)
    return None

def find_multiple_paths(grid, start, end, max_paths=5):
    # 최초 경로
    for row in grid:
        for node in row:
            node.g = float('inf')
            node.f = float('inf')
            node.prev = None
            node.update_neighbors(grid)

    base_path = a_star_path(grid, start, end, set())
    if not base_path:
        print("❌ 첫 경로 없음")
        return []

    paths = [(base_path, PATH_COLORS[0])]
    seen = {tuple(n.get_pos() for n in base_path)}

    for k in range(1, max_paths):
        found = False
        for i in range(1, len(base_path) - 1):  # 시작/끝 제외
            spur_node = base_path[i]
            r, c = spur_node.get_pos()
            original_color = grid[r][c].color
            grid[r][c].make_obstacle()

            for row in grid:
                for node in row:
                    node.g = float('inf')
                    node.f = float('inf')
                    node.prev = None
                    node.update_neighbors(grid)

            new_path = a_star_path(grid, start, end, set())
            if new_path:
                key = tuple(n.get_pos() for n in new_path)
                if key not in seen:
                    paths.append((new_path, PATH_COLORS[k]))
                    seen.add(key)
                    found = True
                    base_path = new_path
                    break

            grid[r][c].color = original_color  # 되돌리기

        if not found:
            break

    return paths

def main():
    grid = make_grid()
    start = end = None
    running = True

    while running:
        draw_all(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # 왼쪽 클릭
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_obstacle()

            elif pygame.mouse.get_pressed()[2]:  # 오른쪽 클릭
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                node.reset()
                if node == start: start = None
                elif node == end: end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.g = float('inf')
                            node.f = float('inf')
                            node.prev = None
                            node.update_neighbors(grid)
                    paths = find_multiple_paths(grid, start, end, max_paths=5)
                    for path, color in paths:
                        for node in path:
                            if not node.is_start() and not node.is_end():
                                node.color = color

                if event.key == pygame.K_c:
                    start = end = None
                    grid = make_grid()

    pygame.quit()

if __name__ == "__main__":
    main()
