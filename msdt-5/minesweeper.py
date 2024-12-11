import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# Параметры экрана и цвета
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 40
GRID_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Игровые переменные
bombs = []
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
game_over = False

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сапер")


# Функция для генерации мин
def generate_bombs(bomb_count=None):
    global bombs, grid
    bombs.clear()
    total_cells = GRID_SIZE * GRID_SIZE
    if bomb_count is None:
        bomb_count = max(1, total_cells // 5)  # По умолчанию 20% клеток
    while len(bombs) < bomb_count:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in bombs:
            bombs.append((x, y))
            grid[x][y] = -1





# Функция для подсчета соседей мин
def calculate_neighbors():
    global grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == -1:  # Мина
                continue
            neighbor_count = 0
            for i in range(-1, 2):  # Проверяем соседей по 8 направлениям
                for j in range(-1, 2):
                    nx, ny = x + i, y + j
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if grid[nx][ny] == -1:  # Соседняя клетка с миной
                            neighbor_count += 1
            grid[x][y] = neighbor_count




# Функция для отображения поля
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[x][y]:
                if grid[x][y] == -1:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    text = str(grid[x][y]) if grid[x][y] > 0 else ""
                    font = pygame.font.Font(None, 36)
                    text_surf = font.render(text, True, BLACK)
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


# Функция для открытия клеток

def open_cell(x, y):
    global game_over
    if grid[x][y] == -1:  # Мина
        game_over = True
        return
    revealed[x][y] = True
    if grid[x][y] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not revealed[nx][ny]:
                    open_cell(nx, ny)  # Рекурсивно открываем соседей




# Основной игровой цикл
def main():
    global game_over
    generate_bombs()
    calculate_neighbors()

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = event.pos
                x, y = mx // CELL_SIZE, my // CELL_SIZE

                if grid[x][y] == -1:
                    game_over = True
                    print("Игра окончена. Вы взорвались!")
                else:
                    open_cell(x, y)

        draw_grid()

        if game_over:
            font = pygame.font.Font(None, 48)
            text_surf = font.render("GAME OVER", True, RED)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()


# Запуск игры
if __name__ == "__main__":
    main()
