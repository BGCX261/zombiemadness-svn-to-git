from pygame.locals import *
from pygame.sprite import *
import pygame
class tile(Sprite):
    
    def __init__(self, numx, numy, idInt, wp, pixelDim, gap):
        Sprite.__init__(self)
        self.gap = gap
        self.size = pixelDim
        self.human = False
        self.hasHuman = False
        self.zombie = False
        self.hasZombie = False
        self.x = numx * pixelDim
        self.y = numy * pixelDim
        self.xPos = numx
        self.yPos = numy
        self.num = str(self.x)+","+str(self.y)
        self.type = idInt
        if(self.type == 0):
            self.blocked = False
            self.helipad = False
            self.axis = 'vertical'
            self.imageFile = "images/road_vertical.png"
        elif(self.type == 1):
            self.blocked = False
            self.helipad = False
            self.axis = 'horizontal'
            self.imageFile = "images/road_horizontal.png"
        elif(self.type == 2):
            self.blocked = True
            self.helipad = False
            self.imageFile = "images/building.png"
        elif(self.type == 3):
            self.blocked = False
            self.helipad = True
            WP_ID = 'F'
            self.imageFile = "images/helipad.png"
        if(wp == 0):
            self.isWaypoint = False
            self.WP_ID = 0
        else:
            self.isWaypoint = True
            self.WP_ID = wp
            self.imageFile = "images/crossroad.png"
        self.Graphics()
    def north(self, array, distance = 1):
        if(self.yPos == 0):
            return False
        else:
            return array[self.yPos-distance][self.xPos]
    def south(self, array, distance = 1):
        if(self.yPos == 19):
            return False
        else:
            return array[self.yPos+distance][self.xPos]
    def east(self, array, distance = 1):
        if(self.xPos == 19):
            return False
        else:   
            return array[self.yPos][self.xPos+distance]
    def west(self, array, distance = 1):
        if(self.xPos == 0):
            return False
        else:
            return array[self.yPos][self.xPos-distance]

    def checkValidDir(self,array):
         directionList = [0,0,0,0]
         if(self.north(array) != False and self.north(array).blocked == False):
             directionList[0]=1
         if(self.south(array) != False and self.south(array).blocked == False):
             directionList[1]=1
         if(self.east(array) != False and self.east(array).blocked == False):
             directionList[2]=1
         if(self.west(array) != False and self.west(array).blocked == False):
             directionList[3]=1
         return directionList
    
    def printMe(self):
        return "current tile is:" + "["+str(self.yPos)+"]["+str(self.xPos)+"]"

    """
    def drawMe(self):
        this = box(pos=(self.x, self.y, 0))
        this.length = 95    
        this.width = 1
        this.height = 95
        this.color=self.colour
    """
    def Graphics(self):
        self.image = pygame.image.load(self.imageFile)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
