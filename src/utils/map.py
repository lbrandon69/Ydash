import csv
import pygame
from pathlib import Path
from utils.obstacles import Platform, Coin, Spike, End

def init_level(map, elements):
    """
    Initialise le niveau à partir de la carte fournie.

    Cette fonction parcourt la carte et place les différents objets à leurs positions respectives. 
    Elle retourne également la position de l'élément "End" s'il est trouvé.

    Args:
        map (list): Carte du niveau sous forme de liste de listes de chaînes de caractères.
        elements (pygame.sprite.Group): Groupe de sprites où les éléments du niveau seront ajoutés.

    Returns:
        tuple: Position (x, y) de l'élément "End" si trouvé, sinon None.
    """
    end_position = None
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            position = (x * 32, y * 32)
            if tile == "End":
                end_position = position 
                element = End(None, position, elements)
            elif tile == "0":
                Platform(None, position, elements)
            elif tile == "Coin":
                Coin("./data/img/Coins/coin_01.png", position, elements)
            elif tile == "Spike":
                Spike(None, position, elements)

    return end_position 

def block_map(level_num):
    """
    Charge une carte de niveau à partir d'un fichier CSV.

    Cette fonction ouvre le fichier CSV correspondant au numéro du niveau 
    et retourne la carte du niveau sous forme de liste de listes de chaînes 
    de caractères représentant chaque case du niveau.

    Args:
        level_num (str): Le nom du fichier CSV représentant le niveau.

    Returns:
        list: La carte du niveau, représentée par une liste de listes de chaînes.
    """
    base_path = Path(__file__).resolve().parent.parent.parent
    level_path = base_path / level_num
    lvl = []
    with open(level_path, newline='') as csvfile:
        trash = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in trash:
            lvl.append(row)
    return lvl

def draw_editor_grid(screen, grid, tile_size, offset_x):
    """
    Dessine la grille d'édition et les éléments du niveau.

    Cette fonction dessine la grille de tuiles ainsi que les éléments placés 
    dans la carte du niveau. Elle prend également en compte un décalage horizontal 
    lors du dessin de la grille.

    Args:
        screen (pygame.Surface): La surface sur laquelle dessiner la grille et les éléments.
        grid (list): La carte du niveau, représentée par une liste de listes.
        tile_size (int): La taille des tuiles dans la grille.
        offset_x (int): Le décalage horizontal de la vue du niveau, permettant de faire défiler la carte.
    """
    screen.fill((0, 0, 0))

    start_col = offset_x // tile_size
    offset_remainder = offset_x % tile_size

    for x in range(-offset_remainder, screen.get_width(), tile_size):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, screen.get_height()))

    for y in range(0, screen.get_height(), tile_size):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (screen.get_width(), y))

    sprite_group.empty()

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col != -1:
                screen_x = col_idx * tile_size - offset_x
                screen_y = row_idx * tile_size
                if 0 <= screen_x < screen.get_width():
                    if col == "0": 
                        platform = Platform(None, (screen_x, screen_y), pygame.sprite.Group())
                        sprite_group.add(platform) 
                    elif col == "Coin":  
                        coin = Coin("./data/img/Coins/coin_01.png", (screen_x, screen_y), pygame.sprite.Group())  
                        sprite_group.add(coin) 
                    elif col == "Spike":
                        spike = Spike(None, (screen_x, screen_y), pygame.sprite.Group()) 
                        sprite_group.add(spike) 
                    elif col == "End":
                        end = End(None, (screen_x, screen_y), pygame.sprite.Group()) 
                        sprite_group.add(end) 
