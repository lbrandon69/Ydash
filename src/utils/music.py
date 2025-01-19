import pygame

# Charger et jouer la musique de fond
def play_music(path):
    pygame.mixer.music.load(path)  # Charger la musique
    pygame.mixer.music.set_volume(0.5)  # Régler le volume de la musique
    pygame.mixer.music.play(loops=-1, start=0.0)  # Lire la musique en boucle

def stop_music():
    pygame.mixer.music.stop()

