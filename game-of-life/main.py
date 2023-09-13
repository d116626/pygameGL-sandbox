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
for i in range(min(W, H)):
    current_field[i, i] = 1
    current_field[i, W - i - 1] = 1

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
