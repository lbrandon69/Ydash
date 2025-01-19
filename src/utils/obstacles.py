import pygame

class Platform(pygame.sprite.Sprite):
    """
    Représente une plateforme dans le jeu.

    Cette classe crée une plateforme simple de taille 32x32 pixels avec une couleur de fond bleue 
    et une bordure bleue plus foncée. Elle est ajoutée au groupe de sprites passé en argument.

    Args:
        image (str): Le chemin de l'image de la plateforme.
        position (tuple): Position de la plateforme dans le jeu sous forme de (x, y).
        group (pygame.sprite.Group): Le groupe de sprites auquel ajouter la plateforme.
    """
    def __init__(self, image, position, group):
        super().__init__(group)
        self.width, self.height = 32, 32
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 127, 255))
        border_color = (0, 97, 255)
        pygame.draw.rect(self.image, border_color, (0, 0, self.width, self.height), 2) 
        self.rect = self.image.get_rect(topleft=position)


class Coin(pygame.sprite.Sprite):
    """
    Représente une pièce collectable dans le jeu.

    Cette classe crée une pièce sous forme d'une image de taille 32x32 pixels, centrée dans un carré de la même taille.
    Elle est ajoutée au groupe de sprites passé en argument.

    Args:
        image (str): Le chemin de l'image de la pièce à afficher.
        position (tuple): Position de la pièce dans le jeu sous forme de (x, y).
        group (pygame.sprite.Group): Le groupe de sprites auquel ajouter la pièce.
    """
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        loaded_image = pygame.image.load(image).convert_alpha()
        scaled_image = pygame.transform.scale(loaded_image, (32, 32))
        
        x_offset = (32 - scaled_image.get_width()) // 2
        y_offset = (32 - scaled_image.get_height()) // 2
        
        self.image.blit(scaled_image, (x_offset, y_offset))
        self.rect = self.image.get_rect(topleft=position)

class Spike(pygame.sprite.Sprite):
    """
    Représente un piège à pointes dans le jeu.

    Cette classe crée une image de type triangle rouge pour simuler un pic, qui peut blesser le joueur.
    La forme est dessinée à l'aide de coordonnées de triangle. Elle est ajoutée au groupe de sprites passé en argument.

    Args:
        image (str): Non utilisé, mais peut être étendu pour charger une image de pic si nécessaire.
        position (tuple): Position du pic dans le jeu sous forme de (x, y).
        group (pygame.sprite.Group): Le groupe de sprites auquel ajouter le pic.
    """
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image, 
            (255, 0, 0),
            [(16, 0), (0, 30), (30, 30)]
        )
        self.rect = self.image.get_rect(topleft=(position[0], position[1] + 2))

class End(pygame.sprite.Sprite):
    """
    Représente l'élément de fin du niveau.

    Cette classe crée un carré bleu de taille 32x32 pixels représentant la fin du niveau.
    Lorsque le joueur atteint cette position, le niveau est terminé. Elle est ajoutée au groupe de sprites passé en argument.

    Args:
        image (str): Non utilisé ici, mais pourrait être utilisé pour afficher une image de fin si nécessaire.
        position (tuple): Position de la fin du niveau dans le jeu sous forme de (x, y).
        group (pygame.sprite.Group): Le groupe de sprites auquel ajouter l'élément de fin.
    """
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=position)
