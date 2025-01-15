import csv
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

