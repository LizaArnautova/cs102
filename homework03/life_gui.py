import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen = pygame.display.set_mode((self.height, self.width))


def draw_lines(self) -> None:
    # Copy from previous assignment
    for x in range(0, self.width, self.cell_size):
        pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
    for y in range(0, self.height, self.cell_size):
        pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for y in range(self.cell_width):
            for x in range(self.cell_height):
                if self.grid[x][y] == 0:
                    rect = (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, pygame.Color('white'), rect)
                else:
                    rect = (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, pygame.Color('green'), rect)

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(self)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
