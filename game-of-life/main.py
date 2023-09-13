import pygame
from random import randint
from copy import deepcopy
import numpy as np
from numba import njit

RES = WIDTH, HEIGHT = 1500, 900
TILE = 4
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 20

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


next_field = np.zeros((H, W), dtype=int)
current_field = deepcopy(next_field)

# current_field = [[0 for i in range(W)] for j in range(H)]
# current_field = [[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)]
# current_field = [[randint(0, 1) for i in range(W)] for j in range(H)]
# current_field = [[1 if not i % 9 else 0 for i in range(W)] for j in range(H)] # 2,5,8,9,10,11,13,18,21,22,26,30,33,65
# current_field = [[1 if not (2 * i + j) % 4 else 0 for i in range(W)] for j in range(H)] # (2,4),(4,4)
# current_field = [[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)] # 5,6,9,22,33
# current_field = np.array([[1 if not i % 7 else randint(0, 1) for i in range(W)] for j in range(H)])
pattern = [
    (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1),
    (4, 0), (4, 1), (5, 0), (5, 1), (6, 0), (6, 1), (7, 0),
    (7, 1), (8, 0), (8, 1), (9, 0), (9, 1), (10, 0), (10, 1),
    (11, 0), (11, 1), (12, 0)
]

# Calculate the starting position to center the pattern
start_x = (W - 13) // 2
start_y = (H - 1) // 2

# Place the pattern on the grid
for y, x in pattern:
    current_field[start_y + y, start_x + x] = 1


@njit(fastmath=True)
def check_cell(current_field, next_field):
    res = []
    for x in range(1,W-1):
        for y in range(1,H-1):
            count=0
            for j in range(y-1,y+2):
                for i in range(x-1,x+2):
                    if current_field[j][i]==1:
                        count+=1
            if current_field[y][x]==1:
                count-=1
                if count==2 or count==3:
                    next_field[y][x]=1
                    res.append((x,y))
                else:
                    next_field[y][x]=0
            else:
                if count==3:
                    next_field[y][x]=1
                    res.append((x,y))
                else:
                    next_field[y][x]=0
    return next_field, res



while True:
    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [pygame.draw.line(surface, pygame.Color('darkslategray'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pygame.draw.line(surface, pygame.Color('darkslategray'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]
    # draw life
    next_field, res = check_cell(current_field, next_field)
    [pygame.draw.rect(surface, pygame.Color('darkorange'), (x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1)) for x, y in res]
    current_field = deepcopy(next_field)

    # print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)
