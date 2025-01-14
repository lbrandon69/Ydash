import pygame
import sys

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
    button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 50)

    while True:
        screen.fill(BLACK)

        draw_text("YDash", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if draw_button(screen, "Jouer", button_play, GRAY, BLUE, font, mouse_pos, mouse_click):
            start_game()
        if draw_button(screen, "Choisir un niveau", button_levels, GRAY, BLUE, font, mouse_pos, mouse_click):
            choose_level()
        if draw_button(screen, "Quitter", button_quit, GRAY, BLUE, font, mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def start_game():
    running = True
    while running:
        screen.fill(BLUE)
        draw_text("Jeu", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def choose_level():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Sélection des niveaux", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

if __name__ == "__main__":
    main_menu()
