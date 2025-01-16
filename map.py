import csv
import pygame
from obstacles import Platform, Coin, Spike, End

def init_level(map, elements):
    x = 0
    y = 0

    for row in map:
        for col in row:

            if col == "0":
                Platform(None, (x, y), elements)  

            if col == "Coin":
                Coin(None, (x, y), elements) 

            if col == "Spike":
                Spike(None, (x, y), elements) 

            if col == "End":
                End(None, (x, y), elements) 

            x += 32 
        y += 32
        x = 0

def block_map(level_num):
    lvl = []
    with open(level_num, newline='') as csvfile:
        trash = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in trash:
            lvl.append(row)
    return lvl

def draw_editor_grid(screen, grid, tile_size, offset_x):
    screen.fill((0, 0, 0))

    start_col = offset_x // tile_size
    offset_remainder = offset_x % tile_size

    for x in range(-offset_remainder, screen.get_width(), tile_size):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, screen.get_height()))

    for y in range(0, screen.get_height(), tile_size):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (screen.get_width(), y))

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col != -1:
                color = {
                    "0": (0, 255, 0),       
                    "Coin": (255, 255, 0), 
                    "Spike": (255, 0, 0),   
                    "End": (0, 0, 255),     
                }.get(col, (255, 255, 255))
                screen_x = col_idx * tile_size - offset_x
                screen_y = row_idx * tile_size
                if 0 <= screen_x < screen.get_width():
                    pygame.draw.rect(
                        screen,
                        color,
                        (screen_x, screen_y, tile_size, tile_size),
                    )