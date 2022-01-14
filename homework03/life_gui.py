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
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, x), (self.height, x))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (y, 0), (y, self.width))

    def draw_grid(self) -> None:
        for y, row in enumerate(self.life.curr_generation):
            y *= self.cell_size
            for x, cell in enumerate(row):
                x *= self.cell_size
                if cell:
                    rect = y, x, self.cell_size, self.cell_size
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)
                else:
                    rect = y, x, self.cell_size, self.cell_size
                    pygame.draw.rect(self.screen, pygame.Color("white"), rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        mouse_click = False

        while running and not self.life.is_max_generations_exceeded and self.life.is_changing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    paused = not paused

                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
                    click_coord = pygame.mouse.get_pos()

            if paused:
                if mouse_click:
                    y = click_coord[0] // self.cell_size
                    x = click_coord[1] // self.cell_size
                    status = self.life.curr_generation[y][x]

                    if status:
                        self.life.curr_generation[y][x] = 0
                    else:
                        self.life.curr_generation[y][x] = 1

                    mouse_click = False
            else:
                self.life.step()

            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((40, 15), max_generations=10)
    gui = GUI(life)
    gui.run()
