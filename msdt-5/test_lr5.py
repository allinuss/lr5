import pytest
from unittest.mock import patch
import minesweeper


def test_generate_bombs():
    minesweeper.bombs = []
    minesweeper.GRID_SIZE = 10  # Размер сетки
    minesweeper.grid = [[0 for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]
    minesweeper.generate_bombs(bomb_count=16)
    assert len(minesweeper.bombs) == 16, "Количество мин должно быть ровно 16"


def test_calculate_neighbors():
    minesweeper.grid = [[0 for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]
    minesweeper.grid[1][1] = -1  # Установим мину
    minesweeper.calculate_neighbors()
    assert minesweeper.grid[0][0] == 1, "Клетка (0, 0) должна иметь одного соседа с миной"
    assert minesweeper.grid[2][2] == 1, "Клетка (2, 2) должна иметь одного соседа с миной"
    assert minesweeper.grid[1][1] == -1, "Клетка с миной не должна изменяться"


def test_open_cell():
    minesweeper.revealed = [[False for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]
    minesweeper.grid = [[0 for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]
    minesweeper.open_cell(0, 0)
    assert minesweeper.revealed[0][0], "Клетка (0, 0) должна быть открыта"
    assert all(minesweeper.revealed[x][y] for x in range(2) for y in range(2)), \
        "Все соседние клетки (в радиусе 1) должны быть открыты"


@pytest.mark.parametrize(
    "grid_size, expected_bombs",
    [(10, 16), (5, 5), (20, 40)]
)
def test_generate_bombs_parametrized(grid_size, expected_bombs):
    minesweeper.GRID_SIZE = grid_size
    minesweeper.bombs = []
    minesweeper.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    minesweeper.generate_bombs(bomb_count=expected_bombs)
    assert len(minesweeper.bombs) == expected_bombs, f"Для сетки {grid_size}x{grid_size} ожидается {expected_bombs} мин"


def test_calculate_neighbors_mock():
    mocked_grid = [[0, -1], [0, 0]]  # Фиксированная тестовая сетка
    with patch("minesweeper.grid", mocked_grid), patch("minesweeper.GRID_SIZE", 2):
        minesweeper.calculate_neighbors()
        assert mocked_grid[0][0] == 1, "Клетка (0, 0) должна показывать 1 мину-соседа"
        assert mocked_grid[1][0] == 1, "Клетка (1, 0) должна показывать 1 мину-соседа"
        assert mocked_grid[0][1] == -1, "Клетка с миной не должна изменяться"


def test_game_over_on_bomb():
    minesweeper.game_over = False
    minesweeper.bombs = [(0, 0)]
    minesweeper.grid = [[0 for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]
    minesweeper.grid[0][0] = -1
    minesweeper.revealed = [[False for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]

    minesweeper.open_cell(0, 0)
    assert minesweeper.game_over, "Игра должна завершиться при открытии клетки с миной"


def test_neighbor_display():
    minesweeper.game_over = False
    minesweeper.bombs = [(1, 1)]
    minesweeper.grid = [[0 for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]
    minesweeper.grid[1][1] = -1
    minesweeper.calculate_neighbors()
    minesweeper.revealed = [[False for _ in range(minesweeper.GRID_SIZE)] for _ in range(minesweeper.GRID_SIZE)]

    minesweeper.open_cell(0, 0)  
    assert minesweeper.revealed[0][0], "Клетка (0, 0) должна быть открыта"
    assert minesweeper.grid[0][0] == 1, "Клетка (0, 0) должна показывать 1 мину-соседа"
