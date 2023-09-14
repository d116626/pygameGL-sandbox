import pygame as pg
import numpy as np
from numba import njit

RES = WIDTH, HEIGHT = 1500, 900
TILE = 2
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 30


class GameOfLife:
    def __init__(self):
        self.current_field = np.zeros((H, W), dtype=int)
        self.next_field = np.zeros((H, W), dtype=int)
        self.is_game_running = False

        x_length = min(W, H) // 2
        center_x = W // 2
        center_y = H // 2

        for i in range(-x_length, x_length + 1):
            x1 = center_x + i
            y1 = center_y + i
            x2 = center_x - i
            y2 = center_y + i

            if 0 <= x1 < W and 0 <= y1 < H:
                self.current_field[y1, x1] = 1
            if 0 <= x2 < W and 0 <= y2 < H:
                self.current_field[y2, x2] = 1

    def toggle_running(self):
        self.is_game_running = not self.is_game_running

    @staticmethod
    @njit(fastmath=True)
    def check_cell(current_field, next_field):
        res = []
        for x in range(1, W - 1):
            for y in range(1, H - 1):
                count = 0
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if current_field[j][i] == 1:
                            count += 1
                if current_field[y][x] == 1:
                    count -= 1
                    if count == 2 or count == 3:
                        next_field[y][x] = 1
                        res.append((x, y))
                    else:
                        next_field[y][x] = 0
                else:
                    if count == 3:
                        next_field[y][x] = 1
                        res.append((x, y))
                    else:
                        next_field[y][x] = 0
        return next_field, res

    def update(self):
        if self.is_game_running:
            self.next_field, res = self.check_cell(self.current_field, self.next_field)
            self.current_field = np.copy(self.next_field)
            self.res = res

    def draw(self, surface):
        surface.fill(pg.Color("black"))

        for y in range(H):
            for x in range(W):
                if self.current_field[y][x] == 1:
                    pg.draw.rect(
                        surface,
                        pg.Color("darkorange"),
                        (x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1),
                    )

        [
            pg.draw.line(surface, pg.Color("black"), (x, 0), (x, HEIGHT))
            for x in range(0, WIDTH, TILE)
        ]
        [
            pg.draw.line(surface, pg.Color("black"), (0, y), (WIDTH, y))
            for y in range(0, HEIGHT, TILE)
        ]

        if hasattr(self, "res"):
            [
                pg.draw.rect(
                    surface,
                    pg.Color("darkorange"),
                    (x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1),
                )
                for x, y in self.res
            ]


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.game_of_life = GameOfLife()

    def run(self):
        while True:
            self.handle_events()
            self.game_of_life.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.game_of_life.toggle_running()

    def draw(self):
        self.surface.fill(pg.Color("black"))
        self.game_of_life.draw(self.surface)
        pg.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
