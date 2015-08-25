import pygame
import random
from pygame.locals import *
from visual import *
from priodict import priorityDictionary
from human import Human
from tile import tile
#---------------------------
#http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466
#---------------------------

class Graph():

    
    def __init__(self, mapName, pixelDim, tileGap):
        self.size = pixelDim
        self.gap = tileGap
        self.x = 0
        self.y = 0
        self.arrayY = []
        self.arrayX = []
        self.currentWaypoints = []
        self.nodeCount = 0
        self.wpCount = 0
        self.weightedGraph = {}
        self.spriteGroup = pygame.sprite.Group()
        self.wallSprites = pygame.sprite.Group()
        self.roadSprites = pygame.sprite.Group()
        self.readMap(mapName)
        self.createGraph()

    def getSpriteGroups(self):
        return (self.spriteGroup,self.wallSprites,self.roadSprites)
    
    def readMap(self,mapName):
        mapFile = open(mapName,'r')
        self.x = int(mapFile.readline())
        self.y = int(mapFile.readline())
        line = mapFile.readline()
        lineList = line.split(',')
        for i in range(self.x):
            for j in range(self.y):
                if(lineList[j].isdigit()):
                    a = int(lineList[j])
                    temp = tile(j,i,a,0,self.size, self.gap)
                    self.arrayY.append(temp)
                    self.spriteGroup.add(temp)
                    if(a==2):
                        self.wallSprites.add(temp)
                    else:
                        self.roadSprites.add(temp)
                    self.nodeCount=self.nodeCount+1
                else:
                    self.wpCount = self.wpCount +1
                    wp = 'W'+str(self.wpCount)
                    temp = tile(j,i,0,wp,self.size, self.gap)
                    self.arrayY.append(temp)
                    self.spriteGroup.add(temp)
                    self.currentWaypoints.append(temp)
                    self.nodeCount=self.nodeCount+1
            self.arrayX.append(self.arrayY)
            self.arrayY=[]
            lineList=mapFile.readline().split(',')
            
    def createGraph(self):
        self.weightedGraph = {'W1':{'W2':5,'W13':5},
                         'W2':{'W1':5,'W3':5,'W6':3},
        		 'W3':{'W2':5,'W4':9,'W11':4},
        		 'W4':{'W3':9,'W8':3},
        		 'W5':{'W6':2,'W15':2},
        		 'W6':{'W2':3,'W5':2,'W9':1},
        		 'W7':{'W8':4,'W12':1},
        		 'W8':{'W4':3,'W7':4,'W17':4},
        		 'W9':{'W6':1,'W10':1},
        		 'W10':{'W9':1,'W11':4,'W21':4},
        		 'W11':{'W3':4,'W10':4,'W12':5,'W22':4},
        		 'W12':{'W7':1,'W11':5,'W16':3},
        		 'W13':{'W1':5,'W14':2},
        		 'W14':{'W13':2,'W15':1,'W19':3},
        		 'W15':{'W5':2,'W15':1},
        		 'W16':{'W12':3,'W17':4,'W23':1},
        		 'W17':{'W8':4,'W16':4,'W27':4},
        		 'W18':{'W19':1,'W28':4},
        		 'W19':{'W14':3,'W18':1,'W20':3},
        		 'W20':{'W19':3,'W21':1,'W29':4},
        		 'W21':{'W10':4,'W20':1,'W22':4},
        		 'W22':{'W11':4,'W21':4,'W23':5,'W31':4},
        		 'W23':{'W16':1,'W22':5,'W25':3},
        		 'W24':{'W25':2,'W32':1},
        		 'W25':{'W23':3,'W24':2,'W26':2},
        		 'W26':{'W25':2,'W27':2,'W42':5},
        		 'W27':{'W17':4,'W26':2},
        		 'W28':{'W18':4,'W29':4,'W43':5},
        		 'W29':{'W20':4,'W28':4,'W30':3,'W44':5},
        		 'W30':{'W29':3,'W31':2,'W36':3},
        		 'W31':{'W22':4,'W30':2,'W32':3},
        		 'W32':{'W24':1,'W31':3,'W34':2},
        		 'W33':{'W34':1,'W37':1,'F':1},
        		 'W34':{'W32':2,'W33':1,'W35':1,'F':1},
        		 'W35':{'W34':1,'W38':1,'F':1},
        		 'W36':{'W30':3,'W37':4,'W46':4},
        		 'W37':{'W33':1,'W36':4,'W39':1,'F':1},
        		 'W38':{'W35':1,'W41':1,'F':1},
        		 'W39':{'W37':1,'W40':1,'F':1},
        		 'W40':{'W39':1,'W41':1,'F':1},
        		 'W41':{'W38':1,'W40':1,'W42':3,'F':1},
        		 'W42':{'W26':5,'W41':3},
        		 'W43':{'W28':5,'W44':4},
        		 'W44':{'W29':5,'W43':4,'W45':2},
        		 'W45':{'W44':2,'W46':3},
        		 'W46':{'W36':4,'W45':3},
        		 'F':{'W33':1,'W34':1,'W35':1,'W37':1,'W38':1,'W39':1,'W40':1,'W41':1}}
    
    #def list_connections():
        #currentGraph={}
        #for i in currentWaypoints:
            #currentGraph
            #tempDir = currentWaypoints[i].checkValidDir(arrayX)
            #for j in tempDir:
                #if(tempDir[j]==1):
                    #currentWaypoints[i]
                    
    def placeHuman(self, human,x,y):
        self.arrayX[x][y].human = human
        self.arrayX[x][y].hasHuman = True

    def placeZombie(self, zombie,x,y):
        self.arrayX[x][y].zombie = zombie
        self.arrayX[x][y].hasZombie = True
    
    def find_waypoint(self,wpID):
        for i in range(self.x):
            for j in range(self.y):
                if(self.arrayX[i][j].WP_ID == wpID):
                    return self.arrayX[i][j]


    #-------------------------------------------------------------------------------------------------
    #Finds the closest waypoint to a given tile. Requires it's containing array (arrayX by default).
    #Direction is not currently used.
    #Returns a tuple containing a reference to the nearest waypoint tile object, the cost to get there
    # and a string representation of the direction required to travel.
    #-------------------------------------------------------------------------------------------------
    def find_closest_waypoint(self,tile,array,direction=0):
        if(tile.blocked == True):
            print "Invalid Tile"
        else:
            validDir = tile.checkValidDir(array)
            print validDir
            cost = 1
            while cost < 20:
                if(validDir[0]==1):
                    if(tile.north(array,cost).isWaypoint==True):
                        return tile.north(array,cost)
                if(validDir[1]==1):
                    if(tile.south(array,cost).isWaypoint==True):
                        return tile.south(array,cost)
                if(validDir[2]==1):
                    if(tile.east(array,cost).isWaypoint==True):
                        return tile.east(array,cost)
                if(validDir[3]==1):
                    if(tile.west(array,cost).isWaypoint==True):
                        return tile.west(array,cost)
                cost = cost + 1

    def Dijkstra(self,G,start,end=None):
    	"""
    	Find shortest paths from the start vertex to all
    	vertices nearer than or equal to the end.
    
    	The input graph G is assumed to have the following
    	representation: A vertex can be any object that can
    	be used as an index into a dictionary.  G is a
    	dictionary, indexed by vertices.  For any vertex v,
    	G[v] is itself a dictionary, indexed by the neighbors
    	of v.  For any edge v->w, G[v][w] is the length of
    	the edge.  This is related to the representation in
    	<http://www.python.org/doc/essays/graphs.html>
    	where Guido van Rossum suggests representing graphs
    	as dictionaries mapping vertices to lists of neighbors,
    	however dictionaries of edges have many advantages
    	over lists: they can store extra information (here,
    	the lengths), they support fast existence tests,
    	and they allow easy modification of the graph by edge
    	insertion and removal.  Such modifications are not
    	needed here but are important in other graph algorithms.
    	Since dictionaries obey iterator protocol, a graph
    	represented as described here could be handed without
    	modification to an algorithm using Guido's representation.
    
    	Of course, G and G[v] need not be Python dict objects;
    	they can be any other object that obeys dict protocol,
    	for instance a wrapper in which vertices are URLs
    	and a call to G[v] loads the web page and finds its links.
    	
    	The output is a pair (D,P) where D[v] is the distance
    	from start to v and P[v] is the predecessor of v along
    	the shortest path from s to v.
    	
    	Dijkstra's algorithm is only guaranteed to work correctly
    	when all edge lengths are positive. This code does not
    	verify this property for all edges (only the edges seen
     	before the end vertex is reached), but will correctly
    	compute shortest paths even for some graphs with negative
    	edges, and will raise an exception if it discovers that
    	a negative edge has caused it to make a mistake.
    	"""
    
    	D = {}	# dictionary of final distances
    	P = {}	# dictionary of predecessors
    	Q = priorityDictionary()   # est.dist. of non-final vert.
    	Q[start] = 0
    	
    	for v in Q:
    		D[v] = Q[v]
    		if v == end: break
    		
    		for w in G[v]:
    			vwLength = D[v] + G[v][w]
    			if w in D:
    				if vwLength < D[w]:
    					raise ValueError, \
      "Dijkstra: found better path to already-final vertex"
    			elif w not in Q or vwLength < Q[w]:
    				Q[w] = vwLength
    				P[w] = v
    	
    	return (D,P)
    			
    def shortestPath(self,start,end):
    	"""
    	Find a single shortest path from the given start vertex
    	to the given end vertex.
    	The input has the same conventions as Dijkstra().
    	The output is a list of the vertices in order along
    	the shortest path.
    	"""
    
    	D,P = self.Dijkstra(self.weightedGraph,start,end)
    	Path = []
    	while 1:
    		Path.append(end)
    		if end == start: break
    		end = P[end]
    	Path.reverse()
    	return Path
