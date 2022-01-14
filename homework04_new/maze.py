from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    y, x = coord
    direction = randint(0, 1)
    if direction:
        if x + 1 != len(grid[0]) - 1:
            grid[y][x + 1] = " "
        elif y != 1:
            grid[y - 1][x] = " "
    else:
        if y != 1:
            grid[y - 1][x] = " "
        elif x + 1 != len(grid[0]) - 1:
            grid[y][x + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True):
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

    for index, i in enumerate(empty_cells):
        grid = remove_wall(grid, i)

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
            coordinate = y, line.index("X")
            exits_coordinates.append(coordinate)

    return exits_coordinates


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] != k:
                continue
            if x > 0 and grid[x - 1][y] == 0:
                grid[x - 1][y] = k + 1
            if y > 0 and grid[x][y - 1] == 0:
                grid[x][y - 1] = k + 1
            if x < len(grid) - 1 and grid[x + 1][y] == 0:
                grid[x + 1][y] = k + 1
            if y < len(grid[0]) - 1 and grid[x][y + 1] == 0:
                grid[x][y + 1] = k + 1
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
    k = int(grid[x][y]) - 1
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
    x, y = coord
    if x == 0 and grid[x + 1][y] == "■":
        return True
    if y == 0 and grid[x][y + 1] == "■":
        return True
    if x == len(grid) - 1 and grid[x - 1][y] == "■":
        return True
    if y == len(grid[0]) - 1 and grid[x][y - 1] == "■":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """
    exits = get_exits(grid)

    # выходов два?
    if len(exits) == 1:
        return grid, exits

    in_cord, out_cord = exits

    # мы в тупике?
    if encircled_exit(grid, in_cord) or encircled_exit(grid, out_cord):
        return grid, None

    grid[in_cord[0]][in_cord[1]], grid[out_cord[0]][out_cord[1]] = 1, 0

    # заполнить всё нулями:
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == " ":
                grid[x][y] = 0

    # найти путь:
    counter = 1
    while grid[out_cord[0]][out_cord[1]] == 0:
        grid = make_step(grid, counter)
        counter += 1

    path = shortest_path(grid, out_cord)
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
        for x, row in enumerate(grid):
            for y, _ in enumerate(row):
                if grid[x][y] != "■":
                    grid[x][y] = " "
                if (x, y) in path:
                    grid[x][y] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
