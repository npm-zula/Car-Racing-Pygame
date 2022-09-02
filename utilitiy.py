import pygame

def scale_image(image, factor):
    size = round(image.get_width() * factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, size)
    

def rotate_image(WINDOW,image,top_left,angle):
    rotated_image = pygame.transform.rotate(image, angle)
    
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    WINDOW.blit(rotated_image,new_rect.topleft)