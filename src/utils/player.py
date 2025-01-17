import pygame
from pygame.math import Vector2
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


        self.rect.x += self.speed_x 
        self.rect.top += self.vel.y

        self.onGround = False

        self.collide(self.vel.y, self.platforms)
