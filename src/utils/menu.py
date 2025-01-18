import pygame
import sys
import csv
import time
from pathlib import Path
from utils.map import block_map, init_level, draw_editor_grid
from utils.player import Player

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
    button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 150, 500, 300, 50)

    click_released = False
    level = 0

    while True:
        screen.fill(BLACK)

        draw_text("YDash", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

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
            elif button_quit.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

            click_released = False  

        draw_button(screen, "Jouer", button_play, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Choisir un niveau", button_levels, GRAY, BLUE, font, mouse_pos, False)
        draw_button(screen, "Crée un niveau", button_create, GRAY, BLUE, font, mouse_pos, False)
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

    levels = ["data/maps/level_1.csv", "data/maps/level_2.csv","data/maps/custom_map.csv"]
    level_data = block_map(levels[level])
    init_level(level_data, elements)

    player_image = pygame.Surface((32, 32))
    player_image.fill((0, 255, 0)) 
    player = Player(player_image, elements, (150, 150), elements)

    clock = pygame.time.Clock()

    while running:
        screen.fill(BLUE)

        scroll_position += scroll_speed
        if scroll_position > len(level_data) * 50:
            scroll_position = 0

        for element in elements:
            element.rect.x -= scroll_speed 

        elements.draw(screen)

        player.update()
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

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)

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