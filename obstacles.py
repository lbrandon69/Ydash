import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=position)

class Coin(pygame.sprite.Sprite):
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 255, 0)) 
        self.rect = self.image.get_rect(topleft=position)

class Spike(pygame.sprite.Sprite):
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=position)

class End(pygame.sprite.Sprite):
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=position)
