import pygame
from pygame.math import Vector2
from utils.obstacles import Platform, Coin, Spike, End

GRAVITY = Vector2(0, 0.5)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, platforms, pos, *groups):
        super().__init__(*groups)
        self.onGround = False 
        self.platforms = platforms  
        self.died = False 
        self.win = False  
        
        self.image = pygame.transform.smoothscale(image, (32, 32))  
        self.rect = self.image.get_rect(center=pos)  
        self.jump_amount = 8
        self.particles = [] 
        self.isjump = False
        self.vel = Vector2(0, 0)

        self.speed_x = 4

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
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.vel.y = 0
                        self.onGround = True
                        self.isjump = False
                    elif yvel < 0:
                        self.rect.top = p.rect.bottom
                    elif self.rect.right > p.rect.left and self.rect.left < p.rect.left:
                        self.died = True
                    else:
                        self.vel.x = 0
                        self.rect.right = p.rect.left

    def jump(self):
        self.vel.y = -self.jump_amount

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

        self.rect.x += self.speed_x 

        self.rect.top += self.vel.y

        self.onGround = False

        self.collide(self.vel.y, self.platforms)