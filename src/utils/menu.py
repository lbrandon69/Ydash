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
from utils.progressBar import draw_stats

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("YDash")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)



def draw_button(surface, text, rect, color, hover_color, font, mouse_pos, mouse_click):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect)
        if mouse_click:
            return True
    else:
        pygame.draw.rect(surface, color, rect)
    draw_text(text, font, WHITE, surface, rect.centerx, rect.centery)
    return False

def main_menu():
    button_play = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 50)
    button_levels = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
    button_create = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 50)
    button_shop = pygame.Rect(SCREEN_WIDTH // 2 - 150, 500, 300, 50)
    button_select_skin = pygame.Rect(SCREEN_WIDTH // 2 - 150, 600, 300, 50)
    button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 150, 700, 300, 50)

    click_released = False
    level = 0

    while True:
        total_coins = load_coins()  # Recharger les pièces à chaque itération
        screen.fill(BLACK)

        draw_text("YDash", font, WHITE, screen, SCREEN_WIDTH // 2, 100)
        draw_text(f"Total Coins: {total_coins}", font, WHITE, screen, SCREEN_WIDTH - 150, 50)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if not mouse_click:
            click_released = True  

        if mouse_click and click_released:
            if button_play.collidepoint(mouse_pos):
                start_game(level)
            elif button_levels.collidepoint(mouse_pos):
                level = choose_level()
            elif button_create.collidepoint(mouse_pos):
                create_level()
            elif button_shop.collidepoint(mouse_pos):
                player = Player("./data/img/Players/skin_01.png", pygame.sprite.Group(), (150, 150))
                shop_menu(player)
            elif button_select_skin.collidepoint(mouse_pos):
                select_skin_menu()
            elif button_quit.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

            click_released = False  

        draw_button(screen, "Jouer", button_play, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Choisir un niveau", button_levels, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Crée un niveau", button_create, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Shop", button_shop, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Sélectionner un skin", button_select_skin, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Quitter", button_quit, GRAY, BLUE, font, mouse_pos, False)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def start_game(level):
    running = True
    elements = pygame.sprite.Group()

    scroll_speed = 4
    scroll_position = 0

    levels = ["data/maps/level_1.csv", "data/maps/level_2.csv", "data/maps/custom_map.csv"]
    level_data = block_map(levels[level])
    
    end_position = init_level(level_data, elements)

    TILE_SIZE = 50
    level_width = len(level_data[0]) * TILE_SIZE

    BASE_BAR_WIDTH = 200
    bar_width = max(BASE_BAR_WIDTH, level_width // 10)

    player_image_path = load_selected_skin()  # Charger le skin sélectionné
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

        if player.died:
            result = lose_screen()
            if result == "menu":
                running = False
            elif result == "replay":
                start_game(level)
        elif player.win:
            result = win_screen()
            if result == "menu":
                running = False
            elif result == "replay":
                start_game(level)

        if end_position:
            progress = min(max((scroll_position + player.rect.x) / (end_position[0]), 0), 1)
        else:
            progress = min(max((scroll_position + player.rect.x) / level_width, 0), 1)

        draw_stats(screen, progress, bar_width)

        # Afficher le compteur de pièces
        draw_text(f"Coins: {player.coins}", font, WHITE, screen, SCREEN_WIDTH - 100, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)

    total_coins = load_coins()
    total_coins += player.coins
    save_coins(total_coins)


def choose_level():
    button_level_1 = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 50)
    button_level_2 = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
    button_custom_game = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 50)

    running = True
    click_released = False  
    selected_level = 0 
    
    while running:
        screen.fill(BLACK)
        draw_text("YDash", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

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

        draw_button(screen, "Level 1", button_level_1, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Level 2", button_level_2, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Custom Level", button_custom_game, GRAY, BLUE, font, mouse_pos, False)

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
    running = True
    TILE_SIZE = 32

    OBJECTS = ["0", "Coin", "Spike", "End"]
    selected_object = 0

    cols = (SCREEN_WIDTH // TILE_SIZE) * 10
    rows = (SCREEN_HEIGHT // TILE_SIZE)
    grid = [[-1 for _ in range(cols)] for _ in range(rows)]
    offset_x = 0

    time.sleep(0.1)

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
                        for row in grid:
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

        draw_editor_grid(screen, grid, TILE_SIZE, offset_x)
        pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 50, 150, 40))
        draw_text(f"Objet: {OBJECTS[selected_object]}", font, BLACK, screen, 85, SCREEN_HEIGHT - 30)

        pygame.display.flip()

def win_screen():
    running = True

    while running:
        screen.fill(BLACK)
        draw_text("Vous avez gagné !", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        
        button_menu = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        button_replay = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if draw_button(screen, "Retour au menu", button_menu, GRAY, BLUE, font, mouse_pos, mouse_click):
            return "menu"
        if draw_button(screen, "Rejouer", button_replay, GRAY, BLUE, font, mouse_pos, mouse_click):
            return "replay"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def lose_screen():
    running = True

    while running:
        screen.fill(BLACK)
        draw_text("Vous avez perdu !", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        button_menu = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        button_replay = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if draw_button(screen, "Retour au menu", button_menu, GRAY, BLUE, font, mouse_pos, mouse_click):
            return "menu"
        if draw_button(screen, "Rejouer", button_replay, GRAY, BLUE, font, mouse_pos, mouse_click):
            return "replay"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def shop_menu(player):
    running = True
    skins = ["skin_01.png", "skin_02.png", "skin_03.png"]
    skin_price = 10
    total_coins = load_coins()
    owned_skins = load_skins()
    selected_skin = load_selected_skin()

    while running:
        screen.fill(BLACK)
        draw_text("Shop", font, WHITE, screen, SCREEN_WIDTH // 2, 100)
        draw_text(f"Total Coins: {total_coins}", font, WHITE, screen, SCREEN_WIDTH - 150, 50)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Display skins
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
                        save_coins(total_coins)  # Sauvegarder les pièces après chaque achat
                        save_skins(skin)  # Sauvegarder le skin acheté
                        owned_skins.append(skin)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def load_coins():
    try:
        with open("coins.json", "r") as file:
            data = json.load(file)
            return data.get("coins", 0)
    except FileNotFoundError:
        return 0

def save_coins(coins):
    with open("coins.json", "w") as file:
        json.dump({"coins": coins}, file)

def load_skins():
    try:
        with open("skins.json", "r") as file:
            data = json.load(file)
            return data.get("skins", [])
    except FileNotFoundError:
        return []

def save_skins(skin):
    skins = load_skins()
    if skin not in skins:
        skins.append(skin)
    with open("skins.json", "w") as file:
        json.dump({"skins": skins}, file)

def load_selected_skin():
    try:
        with open("selected_skin.json", "r") as file:
            data = json.load(file)
            return os.path.join("./data/img/Players", data.get("selected_skin", "skin_01.png"))
    except FileNotFoundError:
        return os.path.join("./data/img/Players", "skin_01.png")

def save_selected_skin(skin):
    with open("selected_skin.json", "w") as file:
        json.dump({"selected_skin": skin}, file)


def select_skin_menu():
    running = True
    owned_skins = load_skins()
    selected_skin = load_selected_skin()
    skin_index = owned_skins.index(selected_skin) if selected_skin in owned_skins else 0

    while running:
        screen.fill(BLACK)
        draw_text("Select Your Skin", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Display the selected skin
        skin_image = pygame.image.load(os.path.join("./data/img/Players", owned_skins[skin_index])).convert_alpha()
        skin_image = pygame.transform.scale(skin_image, (100, 100))
        screen.blit(skin_image, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))

        # Display navigation buttons
        button_prev = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 50, 50)
        button_next = pygame.Rect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2, 50, 50)
        button_select = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 100, 50)

        if draw_button(screen, "<", button_prev, GRAY, BLUE, font, mouse_pos, mouse_click):
            skin_index = (skin_index - 1) % len(owned_skins)
        if draw_button(screen, ">", button_next, GRAY, BLUE, font, mouse_pos, mouse_click):
            skin_index = (skin_index + 1) % len(owned_skins)
        if draw_button(screen, "Select", button_select, GRAY, BLUE, font, mouse_pos, mouse_click):
            selected_skin = owned_skins[skin_index]
            save_selected_skin(selected_skin)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False