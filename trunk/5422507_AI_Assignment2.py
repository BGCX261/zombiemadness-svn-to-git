#---------------------------------
# ZOMBIE OVERLORD
#---------------------------------

class ZombieOverlord
    def __init__(self)
        #list of zombies

    def createZombies(self, zombieNo)
        #fill list of zombies with x zombies, x=zombieNo.

    def updateZombies(self)
        #update all zombies


#---------------------------------
# ZOMBIE CLASS
#---------------------------------

class Zombie
    def __init__(self,startx,starty):
        self.currentx = startx
        self.currenty = starty

    def updateState(self):
        #check if human visible
            #chase
        #else check if other zombies chasing (only visible zombies, should create a landslide effect)
            #chase
        #else
            #roam

    def move(self)
        #if at end of path
            #find new path
        #else
            #move to next point in path

    def findPath(self, target)
        #find best path to target



#---------------------------------
# ZOMBIE STATES
#---------------------------------

class Roaming
    def __init__(self):
        #init

    def roam(self):
        #move around randomly

class Chasing
    def __init__(self):
        #init

    def chase(self):
        #chase human
