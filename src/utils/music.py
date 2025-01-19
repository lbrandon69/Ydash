import pygame

def play_music(path):
    pygame.mixer.music.load(path)  
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(loops=-1, start=0.0)  

def stop_music():
    pygame.mixer.music.stop()

