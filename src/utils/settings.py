import pygame
import sys
from utils.background import draw_star_background

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, 30)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_settings_button(surface, text, rect, color, hover_color, font, mouse_pos, mouse_click):
    image = pygame.image.load("data/img/Logo/settings_01.png")
    image = pygame.transform.scale(image, (40, 40)) 

    pygame.draw.rect(surface, WHITE, rect, border_radius=10)  
    image_rect = image.get_rect(center=rect.center)
    surface.blit(image, image_rect.topleft)

    if rect.collidepoint(mouse_pos):
        if mouse_click:
            return True  
    return False

def draw_close_button(surface, rect, font, mouse_pos, mouse_click):
    pygame.draw.rect(surface, WHITE, rect, border_radius=10)  
    x_text = font.render("X", True, BLACK)
    x_rect = x_text.get_rect(center=rect.center)
    surface.blit(x_text, x_rect.topleft)

    if rect.collidepoint(mouse_pos):
        if mouse_click:
            return True 
    return False

def settings_popup(screen):
    running = True
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()

    popup_width, popup_height = 600, 450
    popup_rect = pygame.Rect((SCREEN_WIDTH - popup_width) // 2, (SCREEN_HEIGHT - popup_height) // 2, popup_width, popup_height)
    close_button = pygame.Rect(popup_rect.right - 50, popup_rect.top + 10, 40, 40)

    game_controls = [
        ("Sauter :", "Espace / Flèche du haut"),
        ("Quitter la partie :", "Échap"),
    ]

    editor_controls = [
        ("Sélection plateforme :", "1"),
        ("Sélection coins :", "2"),
        ("Sélection spike :", "3"),
        ("Sélection end :", "4"),
        ("Pause sélection :", "Clic gauche"),
        ("Supprimer bloc :", "Clic droit"),
        ("Sauvegarder la map :", "S"),
        ("Navigation droite :", "Flèche droite"),
        ("Navigation gauche :", "Flèche gauche"),
        ("Quitter l'éditeur :", "Échap"),
    ]

    small_font = pygame.font.Font(None, 25)
    big_font = pygame.font.Font(None, 35)
    bigest_font = pygame.font.Font(None, 50)

    pop_up_open = False 
    while running:
        screen.fill(BLACK)
        draw_star_background(screen)

        pygame.draw.rect(screen, GRAY, popup_rect, border_radius=15)
        draw_text("Settings", bigest_font, (135,224,45), screen, popup_rect.centerx, popup_rect.top + 30)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0] 

        game_y_offset = popup_rect.top + 70
        draw_text("Commandes du Jeu", big_font, WHITE, screen, popup_rect.centerx, game_y_offset)
        game_y_offset += 20
        for control, action in game_controls:
            draw_text(f"{control} {action}", small_font, WHITE, screen, popup_rect.centerx, game_y_offset)
            game_y_offset += 25

        editor_y_offset = game_y_offset + 15
        draw_text("Commandes de l'Éditeur de Map", big_font, WHITE, screen, popup_rect.centerx, editor_y_offset)
        editor_y_offset += 20
        for control, action in editor_controls:
            draw_text(f"{control} {action}", small_font, WHITE, screen, popup_rect.centerx, editor_y_offset)
            editor_y_offset += 25

        if draw_close_button(screen, close_button, big_font, mouse_pos, mouse_click):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()

def main_with_settings():
    """
    Intègre un bouton dans le menu principal pour ouvrir la fenêtre de paramètres.
    """
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
    pygame.display.set_caption("Settings Example")

    settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 580, 300, 50)

    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if draw_settings_button(screen, "Settings", settings_button, WHITE, BLUE, font, mouse_pos, mouse_click):
            settings_popup(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
