import pygame
import random

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()

class Star(pygame.sprite.Sprite):
    """
    Classe représentant une étoile dans le ciel. L'étoile est un objet sprite avec une taille, une vitesse et un effet de pulsation.
    """
    def __init__(self):
        """
        Initialise une nouvelle étoile avec des propriétés aléatoires pour sa taille, sa position,
        sa vitesse de déplacement et sa vitesse de pulsation.
        """
        super().__init__()
        self.size = random.randint(2, 4) 
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)  
        self.rect.y = random.randint(0, SCREEN_HEIGHT)  
        self.speed = random.randint(1, 2) 
        self.pulse_speed = random.uniform(0.005, 0.02)  
        self.alpha = random.uniform(0.3, 1.0)  

    def update(self):
        """
        Met à jour la position de l'étoile et gère l'effet de pulsation
        de l'étoile.

        Si l'étoile dépasse le bas de l'écran, elle réapparaît en haut à une position aléatoire.
        Le niveau de luminosité de l'étoile oscille entre 0.3 et 1.0.
        """
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-SCREEN_HEIGHT, 0)
            self.rect.x = random.randint(0, SCREEN_WIDTH)

        self.alpha += self.pulse_speed
        if self.alpha >= 1 or self.alpha <= 0.3:
            self.pulse_speed = -self.pulse_speed  

        self.image.set_alpha(int(self.alpha * 255))

def draw_star_background(surface):
    """
    Dessine un fond étoilé animé sur la surface donnée en utilisant des étoiles créées de manière aléatoire.

    Args:
    - surface (pygame.Surface): La surface sur laquelle les étoiles seront dessinées (généralement l'écran du jeu).
    """
    stars = pygame.sprite.Group()
    num_stars = 200  
    
    for _ in range(num_stars):
        star = Star()
        stars.add(star)
    
    stars.update()
    stars.draw(surface)
