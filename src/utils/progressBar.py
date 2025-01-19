import pygame

def draw_stats(screen, progress, bar_width=200):
    """
    Dessine une barre de progression sur l'écran.

    La barre de progression est dessinée sous forme de rectangle. La portion remplie de la barre 
    est déterminée par le paramètre `progress`, qui doit être une valeur entre 0 et 1.

    Args:
        screen (pygame.Surface): L'écran sur lequel dessiner la barre de progression.
        progress (float): La progression du joueur ou du processus, une valeur entre 0 et 1.
        bar_width (int, optional): La largeur de la barre de progression. Par défaut, la largeur est de 200 pixels.

    Returns:
        None
    """
    bar_height = 10
    x = 10
    y = 10 
    pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))  
    pygame.draw.rect(screen, (0, 255, 0), (x, y, progress * bar_width, bar_height)) 