import pygame

class Platform(pygame.sprite.Sprite):
  def __init__(self, image, position, group):
        super().__init__(group)
        self.width, self.height = 32, 32
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 127, 255))
        border_color = (0, 97, 255)
        pygame.draw.rect(self.image, border_color, (0, 0, self.width, self.height), 2)  # Bordure de 2 pixels d'épaisseur
        self.rect = self.image.get_rect(topleft=position)


class Coin(pygame.sprite.Sprite):
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
    def __init__(self, image, position, group):
        super().__init__(group)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=position)
