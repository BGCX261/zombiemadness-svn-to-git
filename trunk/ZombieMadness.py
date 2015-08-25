from graph import Graph
from pygame.locals import *
import random
import pygame
from human import Human
from title import Title
from zombie import Zombie
import time
#------------------------------------------
#PYGAME SHITZ THAT DOESN'T WORK PROPERLY
#------------------------------------------
TILESIZE = 40
HUMANSIZE = 20
ZOMBIESIZE = 20
TILEGAP = 5
SCREENRECT = Rect(0,0,TILESIZE*20,TILESIZE*20)
GameWorld = Graph('map1.map', TILESIZE, TILEGAP)
Player = Human(HUMANSIZE,GameWorld.arrayX[0][15],TILESIZE, GameWorld)

def runGame():
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    
    background = pygame.Surface(SCREENRECT.size).convert()
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    pygame.display.update()
    
    clock = pygame.time.Clock()
    
    spriteGroupList = GameWorld.getSpriteGroups()
    AllSprites = spriteGroupList[0]
    WallSprites = spriteGroupList[1]
    RoadSprites = spriteGroupList[2]

    #for i in range(GameWorld.x):
        #for j in range(GameWorld.y):
            #screen.blit(GameWorld.arrayX[i][j].image, GameWorld.arrayX[i][j].rect)
    AllSprites.draw(screen)
    
    #-testzombie-
    TestZombie1 = Zombie(ZOMBIESIZE,GameWorld.arrayX[3][3],TILESIZE, GameWorld.arrayX)
    TestZombie2 = Zombie(ZOMBIESIZE,GameWorld.arrayX[3][16],TILESIZE, GameWorld.arrayX)
    TestZombie3 = Zombie(ZOMBIESIZE,GameWorld.arrayX[8][5],TILESIZE, GameWorld.arrayX)
    TestZombie4 = Zombie(ZOMBIESIZE,GameWorld.arrayX[9][15],TILESIZE, GameWorld.arrayX)
    TestZombie5 = Zombie(ZOMBIESIZE,GameWorld.arrayX[12][13],TILESIZE, GameWorld.arrayX)
    TestZombie6 = Zombie(ZOMBIESIZE,GameWorld.arrayX[18][5],TILESIZE, GameWorld.arrayX)
    TestZombie7 = Zombie(ZOMBIESIZE,GameWorld.arrayX[18][13],TILESIZE, GameWorld.arrayX)
    zombietimer = 0
    
    #------------
    HealthDisplay = "Health: "+str(Player.health)
    FuelDisplay = "Fuel: "+str(Player.fuel)
    GameWorld.placeHuman(Player, 0,0)
    GameWorld.placeZombie(TestZombie1, 1,1)
    GameWorld.placeZombie(TestZombie2, 1,1)
    GameWorld.placeZombie(TestZombie3, 1,1)
    GameWorld.placeZombie(TestZombie4, 1,1)
    GameWorld.placeZombie(TestZombie5, 1,1)
    GameWorld.placeZombie(TestZombie6, 1,1)
    GameWorld.placeZombie(TestZombie7, 1,1)
    movers = pygame.sprite.RenderPlain(Player,TestZombie1, TestZombie2, TestZombie3, TestZombie4, TestZombie5, TestZombie6, TestZombie7)
    movers.draw(screen)
    #screen.blit(GameWorld.arrayX[0][0].human.image, GameWorld.arrayX[0][0].human.rect)

    pygame.display.update()
    pygame.mixer.music.load("sounds/Contra_Boss_Battle.mid")
    pygame.mixer.music.play(-1)
    mainTitle = Title("images/title.png",150,350)
    titles = pygame.sprite.RenderPlain(mainTitle)
    titles.draw(screen)
    pygame.display.update()
    ENTER = False
    while ENTER is False:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.mixer.music.stop()
            elif (event.type == KEYDOWN and event.key == K_RETURN):
                ENTER = True
            elif (event.type == KEYDOWN and event.key == K_s):
                Player.isSim = True
                ENTER = True
                
    screen.blit(background, (0,0))
    AllSprites.draw(screen)
    movers.draw(screen)
    pygame.display.flip()
    ticks = 0
    while 1:
        font = pygame.font.Font("extras/04b03.TTF", 24)
        HealthText = font.render(HealthDisplay, 0, (230, 0, 0))
        FuelText = font.render(FuelDisplay,0,(230,0,0))
        HealthRect = HealthText.get_rect()
        FuelRect = FuelText.get_rect()
        HealthRect.topleft = [1,SCREENRECT.height-20]
        FuelRect.topleft = [1,SCREENRECT.height-40]
        screen.blit(FuelText, FuelRect)
        screen.blit(HealthText,HealthRect)
        pygame.display.update()        
        clock.tick(30)

        #zombie random timer
        zombietimer = zombietimer + 1
        if zombietimer >= 10:
            zombietimer = 0
            TestZombie1.getNewDirection()
            TestZombie1.move()
            TestZombie2.getNewDirection()
            TestZombie2.move()
            TestZombie3.getNewDirection()
            TestZombie3.move()
            TestZombie4.getNewDirection()
            TestZombie4.move()
            TestZombie5.getNewDirection()
            TestZombie5.move()
            TestZombie6.getNewDirection()
            TestZombie6.move()
            TestZombie7.getNewDirection()
            TestZombie7.move()
            #update hp when zombie moves
            HealthDisplay = "Health: "+str(Player.health)
            Player.updateHealth()
        if(Player.isSim == False):
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.mixer.music.stop()
                    return
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                    or (event.key == K_LEFT)
                    or (event.key == K_UP)
                    or (event.key == K_DOWN)):
                        Player.translateKey(event.key)
                        #update hp when player moves
                        HealthDisplay = "Health: "+str(Player.health)
                        Player.updateHealth()
        else:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.mixer.music.stop()
                    return
            if(ticks == 30):
                Player.doSelfMove()
                #update hp when player moves
                HealthDisplay = "Health: "+str(Player.health)
                Player.updateHealth()

        if Player.health <= 0:
            font = pygame.font.Font("extras/04b03.TTF", 36)
            text = font.render("THE ZOMBIES GOT YOU! GAME OVER!", 0, (230, 0, 0))
            textpos = text.get_rect(centerx=SCREENRECT.width/2,centery=SCREENRECT.height/2)
            screen.blit(text, textpos)
            pygame.display.update()
            pygame.mixer.music.fadeout(5000)
            time.sleep(5)
            return
        if Player.tile.helipad == True:
            font = pygame.font.Font("extras/04b03.TTF", 36)
            text = font.render("CONGRATULATIONS, YOU ESCAPED!", 0, (230, 0, 0))
            textpos = text.get_rect(centerx=SCREENRECT.width/2,centery=SCREENRECT.height/2)
            screen.blit(text, textpos)
            pygame.display.update()
            pygame.mixer.music.fadeout(5000)
            time.sleep(5)
            return
        
        if(ticks == 30):
            ticks = 0
        else:      
            ticks = ticks +1
        movers.update()
        screen.blit(background, (0, 0))
        AllSprites.draw(screen)
        movers.draw(screen)
        pygame.display.flip()

def main():
        runGame()
    
if __name__ == '__main__':main()
