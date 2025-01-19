import pygame
import os
import json
import sys
import csv
import time
import random
from pathlib import Path
from utils.map import block_map, init_level, draw_editor_grid
from utils.player import Player
from utils.background import draw_star_background
from utils.music import play_music, stop_music
from utils.progressBar import draw_stats
from utils.settings import settings_popup, draw_settings_button
from utils.shop import load_coins, save_coins, load_skins, save_skins, load_skins, save_selected_skin, load_selected_skin

pygame.init()
pygame.mixer.init() 

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("YDash")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, 30)

def draw_text(text, font, color, surface, x, y):
    """
    Dessine le texte spécifié à une position donnée sur l'écran.

    Args:
    - text (str): Le texte à afficher.
    - font (pygame.font.Font): La police utilisée pour dessiner le texte.
    - color (tuple): La couleur du texte sous forme de tuple RGB.
    - surface (pygame.Surface): La surface sur laquelle le texte sera dessiné.
    - x (int): La coordonnée x de la position du centre du texte.
    - y (int): La coordonnée y de la position du centre du texte.
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, text, rect, color, hover_color, font, mouse_pos, mouse_click):
    """
    Dessine un bouton avec du texte et gère l'interaction de survol et de clic.

    Args:
    - surface (pygame.Surface): La surface sur laquelle le bouton sera dessiné.
    - text (str): Le texte à afficher sur le bouton.
    - rect (pygame.Rect): Le rectangle qui définit la position et la taille du bouton.
    - color (tuple): La couleur de fond du bouton lorsqu'il n'est pas survolé.
    - hover_color (tuple): La couleur de fond du bouton lorsqu'il est survolé.
    - font (pygame.font.Font): La police utilisée pour le texte du bouton.
    - mouse_pos (tuple): La position actuelle de la souris.
    - mouse_click (bool): True si un clic est effectué, sinon False.

    Returns:
    - bool: True si le bouton a été cliqué, sinon False.
    """
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect, width=0, border_radius=15) 
        if mouse_click:
            return True
    else:
        pygame.draw.rect(surface, color, rect, width=0, border_radius=15) 
    draw_text(text, font, BLACK, surface, rect.centerx, rect.centery)
    return False

def main_menu():
    play_music("data/music/music_01.mp3")
    button_play = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
    button_levels = pygame.Rect(SCREEN_WIDTH // 2 - 150, 370, 300, 50)
    button_create = pygame.Rect(SCREEN_WIDTH // 2 - 150, 440, 300, 50)
    button_shop = pygame.Rect(SCREEN_WIDTH // 2 - 150, 510, 300, 50)
    button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 150, 660, 300, 50)
    button_settings = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)

    click_released = False
    level = 0
    settings_open = False

    while True:
        total_coins = load_coins()  
        screen.fill(BLACK)
        draw_star_background(screen)

        image = pygame.image.load("data/img/Logo/logo_01.png") 
        image = pygame.transform.scale(image, (450, 150))
        screen.blit(image, (SCREEN_WIDTH // 2 - image.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if not mouse_click:
            click_released = True 

        if mouse_click and click_released:
            if button_play.collidepoint(mouse_pos):
                stop_music()
                start_game(level)
            elif button_levels.collidepoint(mouse_pos):
                level = choose_level()
            elif button_create.collidepoint(mouse_pos):
                create_level()
            elif button_shop.collidepoint(mouse_pos):
                player = Player("./data/img/Players/skin_01.png", pygame.sprite.Group(), (150, 150))
                shop_menu(player)
            elif button_quit.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

            click_released = False 

        if draw_settings_button(screen, "Settings", button_settings, WHITE, BLUE, font, mouse_pos, mouse_click):
            settings_open = True

        if settings_open:
            settings_popup(screen) 
            settings_open = False

        draw_button(screen, "Jouer", button_play, WHITE, (135,224,45), font, mouse_pos, False)
        draw_button(screen, "Choisir un niveau", button_levels, WHITE, (135,224,45), font, mouse_pos, False)
        draw_button(screen, "Crée un niveau", button_create, WHITE, (135,224,45), font, mouse_pos, False)
        draw_button(screen, "Shop", button_shop, WHITE, (135,224,45), font, mouse_pos, False)
        draw_button(screen, "Quitter", button_quit, WHITE, (135,224,45), font, mouse_pos, False)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def start_game(level):
    """
    Démarre le jeu avec le niveau spécifié et la musique correspondante.

    Args:
    - level (int): Le niveau à charger.
    """
    running = True
    elements = pygame.sprite.Group()

    scroll_speed = 4
    scroll_position = 0

    levels = ["data/maps/level_1.csv", "data/maps/level_2.csv", "data/maps/custom_map.csv"]
    level_data = block_map(levels[level])

    music_files = [
        "data/music/music_02.mp3",
        "data/music/music_03.mp3",
        "data/music/music_04.mp3"  
    ]
    
    play_music(music_files[level])

    end_position = init_level(level_data, elements)

    TILE_SIZE = 50
    level_width = len(level_data[0]) * TILE_SIZE

    BASE_BAR_WIDTH = 200
    bar_width = max(BASE_BAR_WIDTH, level_width // 10)

    player_image_path = load_selected_skin()  
    player = Player(player_image_path, elements, (150, 150), elements)

    original_background_image = pygame.image.load("./data/img/Backgrounds/background_01.png").convert()  # Utiliser l'arrière-plan sélectionné
    background_image = pygame.transform.scale(
        original_background_image, 
        (original_background_image.get_width(), SCREEN_HEIGHT)
    )
    background_width = background_image.get_width()

    gradient_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(SCREEN_HEIGHT):
        alpha = int((y / SCREEN_HEIGHT) * 100)
        pygame.draw.rect(gradient_surface, (0, 0, 0, alpha), (0, y, SCREEN_WIDTH, 1))

    clock = pygame.time.Clock()

    while running:
        scroll_position += scroll_speed

        for i in range(-1, SCREEN_WIDTH // background_width + 2):
            screen.blit(background_image, (i * background_width - (scroll_position % background_width), 0))
        screen.blit(gradient_surface, (0, 0))

        for element in elements:
            element.rect.x -= scroll_speed

        elements.draw(screen)

        player.update()
        player.update_particles()
        player.draw_particles(screen)

        total_coins = player.coins
        save_coins(total_coins)

        if player.died:
            stop_music()
            result = lose_screen()
            if result == "menu":
                play_music("data/music/music_01.mp3")
                main_menu()
            elif result == "replay":
                play_music(music_files[level])
                start_game(level)
        elif player.win:
            stop_music()
            result = win_screen()
            if result == "menu":
                play_music("data/music/music_01.mp3")
                main_menu()
            elif result == "replay":
                play_music(music_files[level])
                start_game(level)

        if end_position:
            progress = min(max((scroll_position + player.rect.x) / (end_position[0]), 0), 1)
        else:
            progress = min(max((scroll_position + player.rect.x) / level_width, 0), 1)

        draw_stats(screen, progress, bar_width)

        draw_text(f"Coins: {player.coins}", font, BLACK, screen, SCREEN_WIDTH - 100, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_music()
                    running = False
                    play_music("data/music/music_01.mp3")

        clock.tick(60)


def choose_level():
    """
    Permet à l'utilisateur de choisir un niveau parmi les options disponibles.

    Returns:
    - int: Le niveau sélectionné.
    """
    button_level_1 = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
    button_level_2 = pygame.Rect(SCREEN_WIDTH // 2 - 150, 370, 300, 50)
    button_custom_game = pygame.Rect(SCREEN_WIDTH // 2 - 150, 440, 300, 50)

    running = True
    click_released = False  
    selected_level = 0 
    
    while running:
        screen.fill(BLACK)
        draw_star_background(screen)

        image = pygame.image.load("data/img/Logo/logo_01.png") 
        image = pygame.transform.scale(image, (450, 150))
        screen.blit(image, (SCREEN_WIDTH // 2 - image.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if not mouse_click:
            click_released = True

        if mouse_click and click_released:
            if button_level_1.collidepoint(mouse_pos):
                selected_level = 0
                running = False
            elif button_level_2.collidepoint(mouse_pos):
                selected_level = 1
                running = False
            elif button_custom_game.collidepoint(mouse_pos):
                selected_level = 2
                running = False

        draw_button(screen, "Level 1", button_level_1, WHITE, (135,224,45), font, mouse_pos, False)
        draw_button(screen, "Level 2", button_level_2, WHITE, (135,224,45), font, mouse_pos, False)
        draw_button(screen, "Custom Level", button_custom_game, WHITE, (135,224,45), font, mouse_pos, False)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    return selected_level


def create_level():
    """
    Permet à l'utilisateur de créer un niveau personnalisé en plaçant des objets sur une grille.

    Le niveau créé est sauvegardé dans un fichier CSV sous forme de données.
    """
    running = True
    TILE_SIZE = 32

    OBJECTS = ["0", "Coin", "Spike", "End"]
    obj_name = ["Block", "Coin", "Spike", "End"]
    selected_object = 0

    cols = (SCREEN_WIDTH // TILE_SIZE) * 10
    rows = (SCREEN_HEIGHT // TILE_SIZE)
    grid = [[-1 for _ in range(cols)] for _ in range(rows)]
    offset_x = 0

    time.sleep(0.1)
    sprite_group = pygame.sprite.Group()

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = (mouse_pos[0] + offset_x) // TILE_SIZE, mouse_pos[1] // TILE_SIZE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_object = 0
                elif event.key == pygame.K_2:
                    selected_object = 1
                elif event.key == pygame.K_3:
                    selected_object = 2
                elif event.key == pygame.K_4:
                    selected_object = 3
                elif event.key == pygame.K_s:
                    base_path = Path(__file__).resolve().parent.parent.parent
                    level_path = base_path / "data/maps/custom_map.csv"

                    with open(level_path, "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)

                        for col_index in range(len(grid[0])):  
                            start_fill = False
                            for row_index in range(len(grid)):  
                                if grid[row_index][col_index] == "End":
                                    start_fill = True
                                elif start_fill: 
                                    grid[row_index][col_index] = "End"

                            found_end = False
                            for row_index in reversed(range(len(grid))): 
                                if grid[row_index][col_index] == "End":
                                    found_end = True
                                elif found_end: 
                                    grid[row_index][col_index] = "End"

                        for row in grid:
                            last_non_empty = -1
                            for i in range(len(row)):
                                if row[i] != -1: 
                                    last_non_empty = i
                            row = row[:last_non_empty + 1] if last_non_empty != -1 else row
                            writer.writerow(row)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        scroll_speed = TILE_SIZE // 8 
        if keys[pygame.K_RIGHT]:
            offset_x += scroll_speed
        elif keys[pygame.K_LEFT]:
            offset_x = max(0, offset_x - scroll_speed)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if 0 <= mouse_x < cols and 0 <= mouse_y < rows:
                grid[mouse_y][mouse_x] = OBJECTS[selected_object]
        elif mouse_buttons[2]: 
            if 0 <= mouse_x < cols and 0 <= mouse_y < rows:
                grid[mouse_y][mouse_x] = -1

        draw_editor_grid(screen, grid, TILE_SIZE, offset_x, sprite_group)
        pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 50, 150, 40))
        draw_text(f"{obj_name[selected_object]}", font, BLACK, screen, 85, SCREEN_HEIGHT - 30)
        sprite_group.draw(screen)

        pygame.display.flip()


def win_screen():
    """
    Affiche l'écran de victoire et permet de choisir entre revenir au menu ou rejouer.

    Returns:
    - str: "menu" pour retourner au menu, "replay" pour rejouer le niveau.
    """
    running = True

    while running:
        screen.fill(BLACK)
        draw_star_background(screen)
        image = pygame.image.load("data/img/Logo/logo_win.png") 
        image = pygame.transform.scale(image, (933, 86))
        screen.blit(image, (SCREEN_WIDTH // 2 - image.get_width() // 2, 250))
        
        button_replay = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 70, 300, 50)
        button_menu = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if draw_button(screen, "Rejouer", button_replay, WHITE, (135,224,45), font, mouse_pos, mouse_click):
            return "replay"
        if draw_button(screen, "Menu", button_menu, WHITE, (135,224,45), font, mouse_pos, mouse_click):
            return "menu"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def lose_screen():
    """
    Affiche l'écran de défaite et permet de choisir entre revenir au menu ou rejouer.

    Returns:
    - str: "menu" pour retourner au menu, "replay" pour rejouer le niveau.
    """
    running = True

    while running:
        screen.fill(BLACK)
        draw_star_background(screen)
        image = pygame.image.load("data/img/Logo/logo_loose.png") 
        image = pygame.transform.scale(image, (933, 86))
        screen.blit(image, (SCREEN_WIDTH // 2 - image.get_width() // 2, 250))

        button_replay = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 70, 300, 50)
        button_menu = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if draw_button(screen, "Rejouer", button_replay, WHITE, (135,224,45), font, mouse_pos, mouse_click):
            return "replay"
        if draw_button(screen, "Menu", button_menu, WHITE, (135,224,45), font, mouse_pos, mouse_click):
            return "menu"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def shop_menu(player):
    """
    Affiche le menu de la boutique où le joueur peut acheter et sélectionner des skins.

    Args:
    - player: L'objet joueur contenant les informations actuelles du joueur.
    """
    running = True
    skins = ["skin_01.png", "skin_02.png", "skin_03.png"]
    skin_price = 10
    total_coins = load_coins()
    owned_skins = load_skins()
    selected_skin = load_selected_skin()
    button_menu = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 250, 300, 50)

    while running:
        screen.fill(BLACK)
        draw_text("Shop", font, WHITE, screen, SCREEN_WIDTH // 2, 100)
        draw_text(f"Total Coins: {total_coins}", font, WHITE, screen, SCREEN_WIDTH - 200, 50)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for i, skin in enumerate(skins):
            skin_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200 + i * 100, 300, 50)
            skin_image = pygame.image.load(os.path.join("./data/img/Players", skin)).convert_alpha()
            skin_image = pygame.transform.scale(skin_image, (50, 50))
            screen.blit(skin_image, (SCREEN_WIDTH // 2 - 200, 200 + i * 100))
            if skin in owned_skins:
                if draw_button(screen, f"Select Skin {i+1}", skin_rect, GRAY, BLUE, font, mouse_pos, mouse_click):
                    selected_skin = skin
                    save_selected_skin(selected_skin)
            else:
                if draw_button(screen, f"Skin {i+1} - {skin_price} coins", skin_rect, GRAY, BLUE, font, mouse_pos, mouse_click):
                    if total_coins >= skin_price:
                        total_coins -= skin_price
                        save_coins(total_coins)  
                        save_skins(skin)
                        owned_skins.append(skin)

        if draw_button(screen, "Menu", button_menu, WHITE, (135,224,45), font, mouse_pos, mouse_click):
            main_menu()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False