from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


# def remove_wall(
#         grid: List[List[Union[str, int]]], coord: Tuple[int, int]
# ) -> List[List[Union[str, int]]]:
#     """
#
#     :param grid:
#     :param coord:
#     :return:
#     """
#
#     pass


def bin_tree_maze(
        rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for x in range(1, cols, 2):
        for y in range(1, rows - 1, 2):
            if x == 1 and y == rows - 2:
                continue
            elif x == 1:
                direction = 0
            elif y == rows - 2:
                direction = 1
            else:
                direction = randint(0, 1)

            if direction:
                grid[x - 1][y] = " "
            else:
                grid[x][y + 1] = " "

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits_coordinates = []
    for y, line in enumerate(grid):
        x_in_line = line.count("X")
        if x_in_line:
            coordinate = line.index("X"), y
            exits_coordinates.append(coordinate)

    return exits_coordinates


def make_step(grid: List[List[Union[str, int]]], k: int, x_out: int, y_out: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :param x:
    :param y:
    :return:
    """
    while grid[x_out][y_out] == 0:
        start_cord = []
        for x_in, line in enumerate(grid):
            if k in line:
                for h, g in enumerate(line):
                    if g == k:
                        y_in = h
                        cur_cord = x_in, y_in
                        start_cord.append(cur_cord)

        k += 1
        for i in start_cord:
            x_in = i[0]
            y_in = i[1]
            if x_in + 1 < len(grid[0]):
                if grid[x_in + 1][y_in] == 0:
                    grid[x_in + 1][y_in] = k

            if x_in - 1 >= 0:
                if grid[x_in - 1][y_in] == 0:
                    grid[x_in - 1][y_in] = k

            if y_in + 1 < len(grid):
                if grid[x_in][y_in + 1] == 0:
                    grid[x_in][y_in + 1] = k

            if y_in - 1 >= 0:
                if grid[x_in][y_in - 1] == 0:
                    grid[x_in][y_in - 1] = k

    return grid


def shortest_path(
        grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord
    k = grid[x][y] - 1
    path = []
    cur_cord = x, y
    path.append(cur_cord)
    while k > 0:
        if x + 1 < len(grid[0]):
            if grid[x + 1][y] == k:
                cur_cord = x + 1, y
                x += 1

        if x - 1 >= 0:
            if grid[x - 1][y] == k:
                cur_cord = x - 1, y
                x -= 1

        if y + 1 < len(grid):
            if grid[x][y + 1] == k:
                cur_cord = x, y + 1
                y += 1

        if y - 1 >= 0:
            if grid[x][y - 1] == k:
                cur_cord = x, y - 1
                y -= 1

        path.append(cur_cord)
        k -= 1
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    if coord in ((0, 0), (len(grid), len(grid[0])), (0, len(grid[0])), (len(grid), 0)):
        return True  # если в углу

    y, x = coord
    if x == 0 and grid[x + 1][y] == '■':
        return True  # в первой строке
    if x == len(grid) - 1 and grid[len(grid) - 2][y] == '■':
        return True  # в последней строке
    if y == 0 and grid[x][y + 1] == '■':
        return True  # в первом столбце
    if y == len(grid[0]) - 1 and grid[x][len(grid[0]) - 2] == '■':
        return True  # в последнем столбце

    return False


def solve_maze(
        grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    # выходов больше одного?
    if len(get_exits(grid)) == 1:
        return get_exits(grid), grid

    # мы в тупике?
    coord1, coord2 = get_exits(grid)
    if encircled_exit(grid, coord1) or encircled_exit(grid, coord2):
        return None, None

    # поиск решения
    for i in grid:
        for j, h in enumerate(i):
            if h == ' ':
                i[j] = 0
    grid[coord1[1]][coord1[0]] = 1
    grid[coord2[1]][coord2[0]] = 0
    grid = make_step(grid, 1, coord2[1], coord2[0])
    path = shortest_path(grid, (coord2[1], coord2[0]))
    add_path_to_grid(grid, path)
    for i in grid:
        for j, h in enumerate(i):
            if not (h == '■' or h == 'X'):
                i[j] = " "
    return grid, path


def add_path_to_grid(
        grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(20, 20)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
