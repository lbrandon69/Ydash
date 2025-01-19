import pygame
from pygame.math import Vector2
import random
import time
from utils.obstacles import Platform, Coin, Spike, End

GRAVITY = Vector2(0, 0.5)

class Player(pygame.sprite.Sprite):
    """
    Classe représentant le joueur dans le jeu.

    Le joueur est un sprite avec des capacités de saut, de mouvement horizontal, et de gestion des collisions.
    Il peut collecter des pièces, mourir lorsqu'il touche un pic, ou atteindre la fin du niveau. 
    Le joueur génère également des particules lorsqu'il est au sol et se déplace.

    Args:
        image_path (str): Le chemin de l'image du joueur.
        platforms (list): Liste des plateformes dans le niveau avec lesquelles le joueur peut interagir.
        pos (tuple): Position initiale du joueur sous forme de (x, y).
        *groups (pygame.sprite.Group): Groupes auxquels le joueur appartient.
    """
    def __init__(self, image_path, platforms, pos, *groups):
        super().__init__(*groups)
        self.onGround = False
        self.platforms = platforms
        self.died = False
        self.win = False
        self.coins = 0  # Ajouter un compteur de pièces
        
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
        """
        Gère les collisions du joueur avec les plateformes, pièces, pics et la fin du niveau.

        Cette méthode vérifie si le joueur entre en collision avec des éléments du niveau, comme des plateformes,
        des pièces, des pics, et la fin du niveau.

        Args:
            yvel (float): Vitesse verticale du joueur pour la détection des collisions verticales.
            platforms (list): Liste des plateformes sur lesquelles vérifier les collisions.
        """
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Coin):
                    p.kill()
                    self.coins += 1  # Augmenter le compteur de pièces
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
        """
        Permet au joueur de sauter.

        Lorsqu'il est au sol, cette méthode applique une vitesse verticale négative pour simuler un saut.
        """
        self.vel.y = -self.jump_amount
        self.isjump = True

    def create_particle(self):
        """
        Crée une particule sous le joueur, uniquement lorsqu'il est au sol.

        La particule est ajoutée à la liste des particules et a des propriétés aléatoires 
        telles que la taille, la vitesse et la durée de vie.
        """
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
        """
        Met à jour les particules existantes.

        La méthode décrémente la durée de vie des particules, met à jour leur position et leur taille, 
        et supprime celles dont la durée de vie est écoulée.
        """
        for particle in self.particles[:]:
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                continue

            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['size'] = max(0, particle['size'] - 0.1)

    def draw_particles(self, screen):
        """
        Dessine les particules à l'écran.

        Cette méthode parcourt la liste des particules et les dessine avec leurs propriétés actuelles.

        Args:
            screen (pygame.Surface): L'écran sur lequel dessiner les particules.
        """
        for particle in self.particles:
            pygame.draw.rect(
                screen, 
                particle['color'], 
                (particle['pos'][0], particle['pos'][1], particle['size'], particle['size'])
            )

    def update(self):
        """
        Met à jour la position, les collisions, le saut, et les particules du joueur.

        Cette méthode est appelée à chaque itération du jeu. Elle gère les mouvements du joueur, les entrées clavier, 
        la gravité, les collisions avec les plateformes et la génération de particules lorsqu'il se déplace.
        """
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
