from pygame.locals import *
from pygame.sprite import *
import pygame
import random

class Zombie(Sprite):
    
    def __init__(self, zombiesize, tile, tilesize, tileArray):
        """initialize base class"""
        Sprite.__init__(self)
        self.tiles = tileArray
        """Initialize the number of pellets eaten"""
        self.health = 100
        self.fuel = 10
        """Set the number of Pixels to move each time"""
        self.x_dist = tilesize
        self.y_dist = tilesize
        self.size = zombiesize
        """Initialize how much we are moving"""
        self.xMove = 0
        self.yMove = 0
        self.tile = tile
        self.currentDir = "north"
        self.picture = "images/zombie.png"
        self.Graphics()
        """Initialise the next movement direction"""
        self.direction = "north"
        
    def Graphics(self):
        self.image = pygame.image.load(self.picture)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.tile.x+10,self.tile.y+10]
        
    def rotateSprite(self,dir):
        
        if(dir == "east" and self.currentDir != "east"):
            self.image = pygame.image.load(self.picture)
            self.rect = self.image.get_rect()
            oldCentre = self.rect.center
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect()
            self.rect.center = oldCentre
            self.currentDir = "east"
        elif(dir == "west" and self.currentDir != "west"):
            self.image = pygame.image.load(self.picture)
            self.rect = self.image.get_rect()
            oldCentre = self.rect.center
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.center = oldCentre
            self.currentDir = "east"
        elif(dir == "south" and self.currentDir != "south"):
            self.image = pygame.image.load(self.picture)
            self.rect = self.image.get_rect()
            oldCentre = self.rect.center
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.center = oldCentre
            self.currentDir = "south"
        elif(dir == "north" and self.currentDir != "north"):
            self.image = pygame.image.load(self.picture)
            self.rect = self.image.get_rect()
            self.currentDir = "north"

    
                   
    def move(self):
        if (self.direction == "east"):
            if(self.tile.east(self.tiles)==False or self.tile.east(self.tiles).blocked==True):
                self.getNewDirection()
            else:
                self.rotateSprite("east")
                self.tile.hasZombie = False
                self.tile = self.tile.east(self.tiles)
                self.tile.hasZombie = True
        elif (self.direction == "east"):
            if(self.tile.west(self.tiles)==False or self.tile.west(self.tiles).blocked==True):
                self.getNewDirection()
            else:
                self.rotateSprite("west")
                self.tile.hasZombie = False
                self.tile = self.tile.west(self.tiles)
                self.tile.hasZombie = True
        elif (self.direction == "north"):
            if(self.tile.north(self.tiles)==False or self.tile.north(self.tiles).blocked==True):
                self.getNewDirection()
            else:
                self.rotateSprite("north")
                self.tile.hasZombie = False
                self.tile = self.tile.north(self.tiles)
                self.tile.hasZombie = True
               
        elif (self.direction == "south"):
            if(self.tile.south(self.tiles)==False or self.tile.south(self.tiles).blocked==True):
                self.getNewDirection()
            else:
                self.rotateSprite("south")
                self.tile.hasZombie = False
                self.tile = self.tile.south(self.tiles)
                self.tile.hasZombie = True

    def getNewDirection(self):
        self.tempdir = random.randrange(1,4)
        if self.tempdir == 1:
            self.direction = "north"
        elif self.tempdir == 2:
            self.direction = "east"
        elif self.tempdir == 3:
            self.direction = "south"
        elif self.tempdir == 4:
            self.direction = "west"
                
    def update(self):
        self.image.get_rect()
        self.rect.topleft= [self.tile.x+10,self.tile.y+10]
