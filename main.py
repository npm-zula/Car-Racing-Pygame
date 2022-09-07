import pygame
import math
import time
from utilitiy import scale_image, rotate_image

FPS = 60
PATH = [(172, 128), (118, 79), (63, 123), (66, 469), (66, 407), (118, 537), (343, 729), (274, 687), (406, 675), (425, 512), (504, 481), 
(590, 541), (597, 665), (670, 736), (735, 674), (739, 438), (732, 392), (680, 376),(453, 364), (408, 317), (448, 263), (695, 268), (731, 176), 
(687, 71), (553, 74), (385, 65), (286, 125), (287, 257), (281, 359), (230, 403), (172, 348),(130,250) ]

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


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150,200)
    
    def __init__(self, max_velocity, rotation_velocity, path=[]):
        super().__init__(max_velocity, rotation_velocity)
        self.path = path
        self.current_point = 0
        self.vel = max_velocity
        
    def draw_points (self, WINDOW):
        for point in self.path:
            pygame.draw.circle(WINDOW, (255,0,0), point, 5)
    
    def draw(self, WINDOW):
        # self.draw_points(WINDOW)
        super().draw(WINDOW)
        
    def move(self):
        if self.current_point >= len(self.path):
            return
        
        self.calc_angle()
        self.update_path_point()
        super().move()
    
    def calc_angle(self):
        target_x, target_y = self.path[self.current_point]
        xDiff = target_x - self.x
        yDiff = target_y - self.y
        
        if yDiff == 0:
            radianAngle = math.pi/2
        else:
            radianAngle = math.atan(xDiff/yDiff)
            
        if target_y > self.y:
            radianAngle += math.pi
        
        radianAngle = self.angle - math.degrees(radianAngle)
        
        if radianAngle >= 180:
            radianAngle -= 360
        
        if radianAngle > 0:
            self.angle -= min(self.rotation_velocity,abs(radianAngle))
        else:
            self.angle += min(self.rotation_velocity,abs(radianAngle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        
        if rect.collidepoint(*target):
            self.current_point+=1
        
    
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180,200)
    
    def reduceSpeed(self):
        self.vel = max(self.vel - self.acceleration/2,0)
        self.move() 
    
    def collideBounce(self):
        self.vel =- self.vel
        self.move()
    
    
            
        
# functions
def draw(WINDOW, images, playerCar, compCar):
    for img,pos in images:
        WINDOW.blit(img,pos)
    
    playerCar.draw(WINDOW)
    compCar.draw(WINDOW)
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

playerCar = PlayerCar(4, 4)
compCar = ComputerCar(4, 4, PATH)

def handleCollision(playerCar,compCar):
    if playerCar.collide(TRACK_BORDER_MASS) != None:
        playerCar.collideBounce()
    
    comp_finish_intersect_collide = compCar.collide(FINISH_MASK, *FINISH_POS)
    if(comp_finish_intersect_collide != None):
        playerCar.reset()
        compCar.reset()
    
    finish_intersect_collide = playerCar.collide(FINISH_MASK, *FINISH_POS)
    if playerCar.collide(FINISH_MASK, *FINISH_POS):
        if(finish_intersect_collide[1] == 0):
            playerCar.collideBounce()
        else:
            playerCar.reset()
            compCar.reset()
            print("finish")

# running game
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH,(FINISH_POS)), (TRACK_BORDER, (0,0))]


while run:
    clock.tick(FPS)
    
    draw(WINDOW,images,playerCar,compCar)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
    
    keysMove(playerCar)
    compCar.move()
    
    handleCollision(playerCar, compCar)
        
print(compCar.path)
pygame.quit()