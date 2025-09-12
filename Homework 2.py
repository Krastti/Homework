import pygame

pygame.init()

# Палитра цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRID_COLOR = (200, 200, 200)

COLORS = [RED, GREEN, BLUE, WHITE, BLACK]

# Параметры окна
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Homework 2')


# Параметры клеток
WIDTH_GRID, HEIGHT_GRID = 600, 600
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH_GRID // COLS

font = pygame.font.SysFont(None, 24)

grid_colors = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
current_color = BLACK

fill_mode = False

# Отрисовка сетки
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid_colors[row][col], rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

# Отрисовка палитры
def draw_palette():
    palette_x = WIDTH_GRID + 30
    palette_y = 50

    color_size = 30
    spacing = 10
    colors_per_row = 1

    for i, color in enumerate(COLORS):
        row = i // colors_per_row
        col = i % colors_per_row

        x = palette_x + col * (color_size + spacing)
        y = palette_y + row * (color_size + spacing)

        rect = pygame.Rect(x, y, color_size, color_size)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        if color == current_color:
            pygame.draw.rect(screen, color, rect, 4)

# Получение координат клетки по позиции мыши
def get_cell_from_mouse(pos):
    x, y = pos
    if 0 <= x <= WIDTH_GRID and 0 <= y <= HEIGHT_GRID:
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        return row, col
    return None

# Получение цвета из палитры по позиции мыши
def get_color_from_mouse(pos):
    x, y = pos
    if x > WIDTH_GRID + 20:
        palette_x = WIDTH_GRID + 20
        palette_y = 50
        color_size = 30
        spacing = 10
        colors_per_row = 1

        for i, color in enumerate(COLORS):
            row = i // colors_per_row
            col = i % colors_per_row

            color_x = palette_x + col * (color_size + spacing)
            color_y = palette_y + row * (color_size + spacing)

            if (color_x <= x <= color_x + color_size and
                    color_y <= y <= color_y + color_size):
                return color
    return None

# Алгоритм заливки
def flood_fill(start_row, start_col, target_color, replacement_color):

    if target_color == replacement_color:
        return
    if (start_row < 0 or start_row >= ROWS) or (start_col < 0 or start_col >= COLS):
        return
    if grid_colors[start_row][start_col] != target_color:
        return

    grid_colors[start_row][start_col] = replacement_color

    flood_fill(start_row + 1, start_col, target_color, replacement_color)
    flood_fill(start_row - 1, start_col, target_color, replacement_color)
    flood_fill(start_row, start_col + 1, target_color, replacement_color)
    flood_fill(start_row, start_col - 1, target_color, replacement_color)

# Программа
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            cell = get_cell_from_mouse(pos)
            if cell:
                row, col = cell
                target_color = grid_colors[row][col]

                if event.button == 1:
                    grid_colors[row][col] = current_color
                elif event.button == 3:
                    flood_fill(row, col, target_color, current_color)

            selected_color = get_color_from_mouse(pos)
            if selected_color:
                current_color = selected_color

    screen.fill(WHITE)
    draw_grid()
    draw_palette()

    pygame.display.flip()

pygame.quit()