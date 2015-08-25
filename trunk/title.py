import pygame
from pygame.locals import *
from pygame.sprite import *

class Title(Sprite):
    
    def __init__(self,imageName,x,y):
        self.imageFile = imageName
        Sprite.__init__(self)
        self.image = pygame.image.load(imageName)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
