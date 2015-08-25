from pygame.locals import *
from pygame.sprite import *
import pygame

class Human(Sprite):
    
    def __init__(self, humansize, tile, tilesize, world):
        Sprite.__init__(self)
        self.tiles = world.arrayX
        self.isSim = False
        self.gameWorld = world
        self.health = 100
        self.fuel = 10
        self.x_dist = tilesize
        self.y_dist = tilesize
        self.size = humansize
        self.xMove = 0
        self.yMove = 0
        self.moves = 0
        self.moving = False
        self.tile = tile
        self.direction = "none"
        self.nodes = 0
        self.currentDir = "north"
        self.picture = "images/human.png"
        self.Graphics()
        
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
    
    def translateKey(self,key):
        if(key == K_RIGHT):
            self.move("east")
        elif(key == K_LEFT):
            self.move("west")
        elif(key == K_UP):
            self.move("north")
        elif(key == K_DOWN):
            self.move("south")
                   
    def move(self,key):
        if (key == "east"):
            if(self.tile.east(self.tiles)==False or self.tile.east(self.tiles).blocked==True):
                return
            else:
                self.rotateSprite("east")
                self.tile = self.tile.east(self.tiles)
        elif (key == "west"):
            if(self.tile.west(self.tiles)==False or self.tile.west(self.tiles).blocked==True):
                return
            else:
                self.rotateSprite("west")
                self.tile = self.tile.west(self.tiles)
        elif (key == "north"):
            if(self.tile.north(self.tiles)==False or self.tile.north(self.tiles).blocked==True):
                return
            else:
                self.rotateSprite("north")
                self.tile = self.tile.north(self.tiles)              
        elif (key == "south"):
            if(self.tile.south(self.tiles)==False or self.tile.south(self.tiles).blocked==True):
                return
            else:
                self.rotateSprite("south")
                self.tile = self.tile.south(self.tiles)
                
    def update(self):
        self.image.get_rect()
        self.rect.topleft= [self.tile.x+10,self.tile.y+10]

    def updateHealth(self):
        if self.tile.hasZombie == True:
            self.health = self.health - 10                       
            
    def determineDirection(self,wpTile):
        currentX = self.tile.xPos
        currentY = self.tile.yPos
        targetX = wpTile.xPos
        targetY = wpTile.yPos
        if(currentX == targetX and currentY != targetY):
            if(currentY - targetY > 0):
                return ("north", currentY - targetY)
            else:
                return ("south",targetY - currentY)
        elif(currentX != targetX and currentY == targetY):
            if(currentX - targetX > 0):
                return ("west",currentX - targetX)
            else:
                return ("east",targetX - currentX)
            
    def nextMove(self,wpTuple):
        self.path = []
        i = 0  
        while i < wpTuple[1]:
            self.path.append(wpTuple[0])
            i = i+1
        
    def moveAlongPath(self, hopNo):
        if(hopNo < self.maxHops):
            self.nextWaypoint = self.gameWorld.find_waypoint(self.shortestPath[hopNo])
            nextDir = self.determineDirection(self.nextWaypoint)
            self.nextMove(nextDir)
        
    def doSelfMove(self):
            if(self.moving == True): #keep moving
                if(self.tile != self.nextWaypoint):
                    self.move(self.path[self.moves])
                    self.moves = self.moves+1
                elif(self.tile == self.nextWaypoint):
                    self.moves = 0
                    self.hops = self.hops+1
                    self.moveAlongPath(self.hops)
                    self.move(self.path[self.moves])
            elif(self.moving == False): #start moving
                if(self.tile.isWaypoint == False):
                    self.moves = 0
                    self.nextWaypoint = self.gameWorld.find_closest_waypoint(self.tile, self.tiles)
                    nextDir = self.determineDirection(self.nextWaypoint)
                    self.shortestPath = self.gameWorld.shortestPath(self.nextWaypoint.WP_ID,'F')
                    self.maxHops = len(self.shortestPath)-1
                    self.hops = 0
                    self.nextMove(nextDir)
                    self.move(self.path[self.moves])
                    self.moves = self.moves+1
                    self.moving = True
                elif(self.tile.isWaypoint == True):
                    self.shortestPath = self.gameWorld.shortestPath(self.tile.WP_ID, 'F')
                    self.maxHops = len(self.shortestPath)-1
                    self.hops = 1
                    self.moves = 0
                    self.moveAlongPath(self.hops)
                    self.move(self.path[self.moves])
                    self.moving = True