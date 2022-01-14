import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for i in range(self.cols)] for i in range(self.rows)]
        else:
            grid = [[0 for i in range(self.cols)] for i in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        cells = []
        if 0 < x < len(self.curr_generation[0]) - 1 and 0 < y < len(self.curr_generation) - 1:  # центр
            cells = [self.curr_generation[y - 1][x - 1], self.curr_generation[y - 1][x],
                     self.curr_generation[y - 1][x + 1],
                     self.curr_generation[y][x - 1], self.curr_generation[y][x + 1],
                     self.curr_generation[y + 1][x - 1], self.curr_generation[y + 1][x],
                     self.curr_generation[y + 1][x + 1]]

        if x == y and x == 0:
            cells = [self.curr_generation[y][x + 1], self.curr_generation[y + 1][x],
                     self.curr_generation[y + 1][x + 1]]  # лево верх
        if x == 0 and y == len(self.curr_generation) - 1:
            cells = [self.curr_generation[y][x + 1], self.curr_generation[y - 1][x],
                     self.curr_generation[y - 1][x + 1]]  # лево низ
        if x == len(self.curr_generation[0]) - 1 and y == 0:
            cells = [self.curr_generation[y][x - 1], self.curr_generation[y + 1][x - 1],
                     self.curr_generation[y + 1][x]]  # право верх
        if x == len(self.curr_generation[0]) - 1 and y == len(self.curr_generation) - 1:
            cells = [self.curr_generation[y][x - 1], self.curr_generation[y - 1][x - 1],
                     self.curr_generation[y - 1][x]]  # право низ

        if x == 0 and 0 < y < len(self.curr_generation) - 1:  # лево
            cells = [self.curr_generation[y - 1][x], self.curr_generation[y - 1][x + 1], self.curr_generation[y][x + 1],
                     self.curr_generation[y + 1][x],
                     self.curr_generation[y + 1][x + 1]]
        if 0 < x < len(self.curr_generation[0]) - 1 and y == 0:  # вверх
            cells = [self.curr_generation[y][x - 1], self.curr_generation[y][x + 1], self.curr_generation[y + 1][x - 1],
                     self.curr_generation[y + 1][x],
                     self.curr_generation[y + 1][x + 1]]
        if x == len(self.curr_generation[0]) - 1 and 0 < y < len(self.curr_generation) - 1:  # право
            cells = [self.curr_generation[y - 1][x - 1], self.curr_generation[y - 1][x], self.curr_generation[y][x - 1],
                     self.curr_generation[y + 1][x - 1],
                     self.curr_generation[y + 1][x]]
        if 0 < x < len(self.curr_generation[0]) - 1 and y == len(self.curr_generation) - 1:  # низ
            cells = [self.curr_generation[y - 1][x - 1], self.curr_generation[y - 1][x],
                     self.curr_generation[y - 1][x + 1], self.curr_generation[y][x - 1],
                     self.curr_generation[y][x + 1]]

        return cells

    def get_next_generation(self) -> Grid:
        newgrid = []
        for y, row in enumerate(self.curr_generation):
            line = []
            for x, cell in enumerate(row):
                neighbours = self.get_neighbours((y, x))
                if cell == 1 and neighbours.count(1) not in [2, 3]:
                    line.append(0)
                elif cell == 0 and neighbours.count(1) == 3:
                    line.append(1)
                else:
                    line.append(cell)
            newgrid.append(line)
        return newgrid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as inp:
            grid = [[int(cell) for cell in row.strip()] for row in inp]
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as outp:
            for i in self.curr_generation:
                stroka = ""
                for j in i:
                    stroka += str(j)
                outp.write(stroka + "\n")

if __name__ == '__main__':
    game = GameOfLife((5, 6), 20)
    # game = GameOfLife()
    game.save("save.txt")