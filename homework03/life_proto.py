import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Поле
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.

        """
        if randomize:
            grid = [
                [random.randint(0, 1) for i in range(self.cell_width)]
                for j in range(self.cell_height)
            ]
        else:
            grid = [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(self.cell_width):
            for x in range(self.cell_height):
                if self.grid[x][y] == 0:
                    rect = (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, pygame.Color("white"), rect)
                else:
                    rect = (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        y, x = cell
        cells = []
        if 0 < x < len(self.grid[0]) - 1 and 0 < y < len(self.grid) - 1:  # центр
            cells = [
                self.grid[y - 1][x - 1],
                self.grid[y - 1][x],
                self.grid[y - 1][x + 1],
                self.grid[y][x - 1],
                self.grid[y][x + 1],
                self.grid[y + 1][x - 1],
                self.grid[y + 1][x],
                self.grid[y + 1][x + 1],
            ]

        if x == y and x == 0:
            cells = [self.grid[y][x + 1], self.grid[y + 1][x], self.grid[y + 1][x + 1]]  # лево верх
        if x == 0 and y == len(self.grid) - 1:
            cells = [
                self.grid[y][x + 1],
                self.grid[y - 1][x],
                self.grid[y - 1][x + 1],
            ]  # лево низ
        if x == len(self.grid[0]) - 1 and y == 0:
            cells = [
                self.grid[y][x - 1],
                self.grid[y + 1][x - 1],
                self.grid[y + 1][x],
            ]  # право верх
        if x == len(self.grid[0]) - 1 and y == len(self.grid) - 1:
            cells = [
                self.grid[y][x - 1],
                self.grid[y - 1][x - 1],
                self.grid[y - 1][x],
            ]  # право низ

        if x == 0 and 0 < y < len(self.grid) - 1:  # лево
            cells = [
                self.grid[y - 1][x],
                self.grid[y - 1][x + 1],
                self.grid[y][x + 1],
                self.grid[y + 1][x],
                self.grid[y + 1][x + 1],
            ]
        if 0 < x < len(self.grid[0]) - 1 and y == 0:  # вверх
            cells = [
                self.grid[y][x - 1],
                self.grid[y][x + 1],
                self.grid[y + 1][x - 1],
                self.grid[y + 1][x],
                self.grid[y + 1][x + 1],
            ]
        if x == len(self.grid[0]) - 1 and 0 < y < len(self.grid) - 1:  # право
            cells = [
                self.grid[y - 1][x - 1],
                self.grid[y - 1][x],
                self.grid[y][x - 1],
                self.grid[y + 1][x - 1],
                self.grid[y + 1][x],
            ]
        if 0 < x < len(self.grid[0]) - 1 and y == len(self.grid) - 1:  # низ
            cells = [
                self.grid[y - 1][x - 1],
                self.grid[y - 1][x],
                self.grid[y - 1][x + 1],
                self.grid[y][x - 1],
                self.grid[y][x + 1],
            ]

        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        newgrid = []
        for y, row in enumerate(self.grid):
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


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
