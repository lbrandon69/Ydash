import pygame

def draw_stats(screen, progress, bar_width=200):
    bar_height = 10
    x = 10
    y = 10 
    pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))  
    pygame.draw.rect(screen, (0, 255, 0), (x, y, progress * bar_width, bar_height)) 