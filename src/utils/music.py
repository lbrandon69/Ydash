import pygame

def play_music(path):
    """
    Charge et lit de la musique en boucle à partir du chemin spécifié.

    Args:
    - path (str): Le chemin du fichier audio à jouer.
    """
    pygame.mixer.music.load(path)  
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(loops=-1, start=0.0)  

def stop_music():
    """
    Arrête la musique en cours de lecture.
    """
    pygame.mixer.music.stop()

