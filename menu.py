import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("YDash")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)

font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(BLACK)

        draw_text("YDash", font, WHITE, screen, SCREEN_WIDTH // 2, 100)
        draw_text("1. Jouer", font, WHITE, screen, SCREEN_WIDTH // 2, 200)
        draw_text("2. Choisir un niveau", font, WHITE, screen, SCREEN_WIDTH // 2, 250)
        draw_text("3. Quitter", font, WHITE, screen, SCREEN_WIDTH // 2, 350)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game()
                elif event.key == pygame.K_2:
                    choose_level()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def start_game():
    running = True
    while running:
        screen.fill(BLUE)
        draw_text("Jeu", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

def choose_level():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Choix du niveau ", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False