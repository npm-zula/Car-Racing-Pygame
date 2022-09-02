import pygame
import math
import time
from utilitiy import scale_image, rotate_image

FPS = 60

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"),2.5) 
TRACK = scale_image(pygame.image.load("imgs/track.png"),0.9) 
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"),0.9)

FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55) 
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55) 

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CAR RACING GAME")


class AbstractCar:
    IMG = RED_CAR
    
    def __init__(self, max_velocity, rotation_velocity):
        self.img = self.IMG
        self.max_velocity = max_velocity
        self.rotation_velocity = rotation_velocity
        self.angle = 0
        self.vel = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
    
    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity
            
    def draw(self, WINDOW):
        rotate_image(WINDOW, self.img, (self.x, self.y), self.angle )
        
    def moveForword(self):
        self.vel =min(self.vel + self.acceleration, self.max_velocity)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
        
    def reduceSpeed(self):
        self.vel = max(self.vel - self.acceleration/2,0)
        self.move()
    
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180,200)

def draw(WINDOW, images, playerCar):
    for img,pos in images:
        WINDOW.blit(img,pos)
    
    playerCar.draw(WINDOW)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0))]
playerCar = PlayerCar(4, 4)

while run:
    clock.tick(FPS)
    
    draw(WINDOW,images,playerCar)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_a]:
        playerCar.rotate(left=True)
    if keys[pygame.K_d]:
        playerCar.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        playerCar.moveForword()
    
    if not moved:
        playerCar.reduceSpeed()
        
pygame.quit()