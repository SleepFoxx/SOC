import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("high_alert.mp3")

pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)