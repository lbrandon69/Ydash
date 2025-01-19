import pygame
from pygame.math import Vector2
import random
import time
from utils.obstacles import Platform, Coin, Spike, End

GRAVITY = Vector2(0, 0.5)

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, platforms, pos, *groups):
        super().__init__(*groups)
        self.onGround = False
        self.platforms = platforms
        self.died = False
        self.win = False
        
        raw_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.smoothscale(raw_image, (32, 32)) 
        self.image = self.original_image  
        self.rect = self.image.get_rect(center=pos)
        
        self.jump_amount = 8
        self.particles = []
        self.isjump = False
        self.vel = pygame.Vector2(0, 0)

        self.speed_x = 4
        
        self.rotation_angle = 0 
        self.rotation_speed = -8

    def collide(self, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Coin):
                    p.kill()
                elif isinstance(p, Spike):
                    self.died = True 
                elif isinstance(p, End):
                    self.win = True 
                elif isinstance(p, Platform):
                    if self.rect.right > p.rect.left and self.rect.left < p.rect.left:
                        self.died = True
                    elif yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.vel.y = 0
                        self.onGround = True
                        self.isjump = False
                        self.rotation_angle = 0
                    elif yvel < 0:
                        self.rect.top = p.rect.bottom
                    else:
                        self.vel.x = 0
                        self.rect.right = p.rect.left

    def jump(self):
        self.vel.y = -self.jump_amount
        self.isjump = True

    def create_particle(self):
        """Ajoute une particule directement au bord inférieur gauche du joueur, uniquement si le joueur est au sol."""
        if self.isjump == False:
            particle = {
                'pos': [self.rect.left + random.randint(0, 5), self.rect.bottom],  
                'vel': [random.uniform(-2, -0.5), random.uniform(-1, 1)],  
                'size': random.randint(3, 6),
                'color': (255, 255, 255), 
                'lifetime': 30
            }
            self.particles.append(particle)


    def update_particles(self):
        for particle in self.particles[:]:
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                continue

            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['size'] = max(0, particle['size'] - 0.1)

    def draw_particles(self, screen):
        """Dessine les particules sur l'écran."""
        for particle in self.particles:
            pygame.draw.rect(
                screen, 
                particle['color'], 
                (particle['pos'][0], particle['pos'][1], particle['size'], particle['size'])
            )

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if self.onGround and not self.isjump:
                self.isjump = True
                self.jump()

        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100:
                self.vel.y = 100

        self.collide(0, self.platforms)

        if self.isjump:
            self.rotation_angle += self.rotation_speed 

            if self.rotation_speed > 0 and self.rotation_angle > 180:
                self.rotation_angle = 180
            elif self.rotation_speed < 0 and self.rotation_angle < -180:
                self.rotation_angle = -180

            rotated_image = pygame.transform.rotate(self.original_image, self.rotation_angle)

            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.rect.center)

        if self.vel.x != 0 or self.vel.y != 0:
            self.create_particle()

        self.update_particles() 

        self.rect.x += self.speed_x 
        self.rect.top += self.vel.y

        self.onGround = False

        self.collide(self.vel.y, self.platforms)
