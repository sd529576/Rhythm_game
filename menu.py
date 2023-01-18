import pygame
from pygame import mixer

pygame.init()
mixer.init()

mixer.music.load('Rhythm.mp3')
screen = pygame.display.set_mode((800,600))

menu_color = (255,0,0)

screen.fill(menu_color)
pygame.display.flip()