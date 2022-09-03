import pygame
import math
import time
from utilitiy import scale_image, rotate_image

FPS = 60

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"),2.5) 
TRACK = scale_image(pygame.image.load("imgs/track.png"),0.9) 

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"),0.9)
TRACK_BORDER_MASS = pygame.mask.from_surface(TRACK_BORDER)


FINISH = pygame.image.load("imgs/finish.png")
FINISH_POS = (130,250)
FINISH_MASK = pygame.mask.from_surface(FINISH)

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
        
    def moveBackward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_velocity/2)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
    
    def collide(self,mask,x = 0, y = 0):
        carMask = pygame.mask.from_surface(self.img)
        offset = (int(self.x -x ),int(self.y - y))
        intersection = mask.overlap(carMask,offset)
        return intersection
    
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
    
    
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180,200)
    
    def reduceSpeed(self):
        self.vel = max(self.vel - self.acceleration/2,0)
        self.move() 
    
    def collideBounce(self):
        self.vel =- self.vel
        self.move()

def draw(WINDOW, images, playerCar):
    for img,pos in images:
        WINDOW.blit(img,pos)
    
    playerCar.draw(WINDOW)
    pygame.display.update()

def keysMove(playerCar):
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_a]:
        playerCar.rotate(left=True)
    if keys[pygame.K_d]:
        playerCar.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        playerCar.moveForword()
    if keys[pygame.K_s]:
        moved = True
        playerCar.moveBackward()
    
    if not moved:
        playerCar.reduceSpeed()
    


# running game
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH,(FINISH_POS)), (TRACK_BORDER, (0,0))]
playerCar = PlayerCar(4, 4)

while run:
    clock.tick(FPS)
    
    draw(WINDOW,images,playerCar)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keysMove(playerCar)
    if playerCar.collide(TRACK_BORDER_MASS) != None:
        playerCar.collideBounce()
    
    finish_intersect_collide = playerCar.collide(FINISH_MASK, *FINISH_POS)
    if playerCar.collide(FINISH_MASK, *FINISH_POS):
        if(finish_intersect_collide[1] == 0):
            playerCar.collideBounce()
        else:
            playerCar.reset()
            print("finish")
        
    
pygame.quit()