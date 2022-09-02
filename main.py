import pygame
import math
import time
from utilitiy import scale_image

FPS = 60

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"),2.5) 
TRACK = scale_image(pygame.image.load("imgs/track.png"),0.9) 
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"),0.9)

FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = pygame.image.load("imgs/red-car.png")
GREEN_CAR = pygame.image.load("imgs/green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CAR RACING GAME")



run = True
clock = pygame.time.Clock()
while run:
    clock.tick(FPS)
    
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
pygame.quit()