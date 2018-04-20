
import random


class Tile(): 
    def __init__(self, ID, width, height):
        self.x = -50
        self.y = -50
        self.ID = ID
        self.width = width
        self.height = height
        self.color = "#" + ("%06x" % random.randint(0, 16777215))
        self.placed = False
        self.flipped = False
            
    def getX(self): return self.x
    
    def getY(self): return self.y 
    
    def getID(self): return self.ID
    
    def getWidth(self): return self.width
    
    def getHeight(self): return self.height
    
    def getSurface(self): return (self.width * self.height)
    
    def getColor(self): return self.color
            
    def flip(self): 
        self.width, self.height = self.height, self.width
        if self.flipped == False:
            self.flipped = True
        else: self.flipped = False
    
    def getFlipped(self): return self.flipped
    
    def setCoordinates(self, x, y): 
        self.x = x
        self.y = y
                    
    def placeThisTile(self): self.placed = True
    
    def removeThisTile(self): self.placed = False
    
    def getPlaced(self): return self.placed    
    
    ################################################################################################################
    
from tkinter import *
class FieldFrame(object):
    MARGINLEFT = 25
    MARGINTOP = 25
    
    def __init__(self, field, scale):
        self.SCALE = scale
        self.field = field
        
        self.root = Tk()
        
        self.frame = Frame(self.root, width=1024, height=768, colormap="new")
        self.frame.pack(fill=BOTH, expand=1)
#        self.frame.repaint(self.field)
        
        self.label = Label(self.frame, text="Tilling Case")
        self.label.pack(fill=X, expand=1)
        
        self.canvas = Canvas(self.frame,
                             bg="white",
                             width=self.field.getWidth() * self.SCALE + 1,
                             height=self.field.getHeight() * self.SCALE + 1)
        self.canvas.pack()
        
        self.canvas.focus_set()
        
    def setField(self, field):
        for tile in field.getTiles():
            tile = tile[0]
            self.canvas.create_rectangle(tile.getX() * self.SCALE + 2,
                                         tile.getY() * self.SCALE + 2,
                                         (tile.getX() + tile.getWidth()) * self.SCALE + 2,
                                         (tile.getY() + tile.getHeight()) * self.SCALE + 2,
                                         fill=tile.getColor())
        self.canvas.pack()
        self.root.update()

    def repaint(self, field):
        self.canvas.delete("all")
        self.setField(field)
        self.root.after(100)
            
        
####################################################################################################################


class Field(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tileset = []
        self.placedID = []

        self.field = [[0 for y in range(self.height)] for x in range(self.width)]
        
        
    def printField(self):
            tempField=[*zip(*self.field.copy())]
            print("Field")
            for i in range(0, self.height):
                print(tempField[i])

    def __copy__(self):
        return type(self)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getTile(self, index):
        return self.tileset[index]

    def getTiles(self):
        return self.tileset

    def addTile(self, tile, placed, surface):
        self.tileset.append([tile, placed, surface])
    
    
    def sortTilesetDecreasing(self):
       self.tileset = sorted(self.tileset, key=lambda tile: (tile[1],-tile[2]))    
     
    def sortTilesetIncreasing(self):
       self.tileset = sorted(self.tileset, key=lambda tile: (tile[2],-tile[1]))    

    def getNumberOfTiles(self):
        return len(self.tileset)
    
    def getLastPlacedID(self): return self.placedID[-1]
    
    def removeLastPlacedID(self): self.placedID.pop()

    def placeTile(self, tile, x, y):
        if not (x >= self.width or y >= self.height):
            for i in range(tile.getWidth()):
                for j in range(tile.getHeight()):
                    self.field[x + i][y + j] = tile.getID()
            tile.setCoordinates(x, y)
            tile.placeThisTile()
            self.placedID.append(tile.getID())
            for instance in self.tileset:
                if instance[0] == tile:
                    self.tileset.remove(instance)
                    instance[1] = True
                    self.tileset.append(instance)
            return True
        return False

    def tileFits(self, tile, x, y):
        if ((self.width - x >= tile.getWidth()) and (self.height - y >= tile.getHeight())):
            for i in range(tile.getWidth()):
                for j in range(tile.getHeight()):
                    if (self.isOccupied(x + i, y + j)):
                        return False
            return True
        return False

    def removeTile(self, tile):
        for i in range(tile.getWidth()):
            for j in range(tile.getHeight()):
                self.field[tile.getX() + i][tile.getY() + j] = 0
        for instance in self.tileset:
            if instance[0] == tile:
                self.tileset.remove(instance)
                instance[1] = False
                self.tileset.append(instance)
        self.placedID.remove(tile.getID())
        tile.setCoordinates(-50, -50)

    def isOccupied(self, x, y):
        return self.field[x][y] != 0

    def solved(self):
        for x in range(self.getWidth()):
            for y in range(self.getHeight()):
                if not self.isOccupied(x, y): return False
        return True

    def getField(self):
        return self.field

    def isEmpty(self, x, y):
        return self.field[x][y] == 0
    


    #################################################################################################################
    
import sys, numpy
from random import randint
from itertools import groupby

class Assignment():
    
    def __init__(self):
        self.steps = 0
        self.maxFilledPercentage = 0
        self.maxfilledStep = 0
        self.visited_tiles = list()
        self.solution=0
        self.lastTile = Tile(300, 200,200)
        self.tiles = list()
        self.sizes=[]
        self.uniqueSol=[]
        idx = 0

        source="C:/Users/Vlad/Desktop/tilings/15-4-0.tiles"
        for line in open(source):

            line = line.split(' ')
            if idx == 0:
                
                width = line[1]
                height = line[3]
                scale = line[5]
                idx=idx+1
                self.field = Field(int(width), int(height))
                self.frame = FieldFrame(self.field, int(scale))
            else:
                times = line[0]
                line = line[2].split('x')
                width = line[0]
                height = line[1]
                for j in range(int(times)):
                    tile = Tile(idx, int(width), int(height))
                    self.field.addTile(tile, False, tile.getSurface())
                    idx=idx+1


        self.dfsAlgorithmSorted(self.visited_tiles, 0, len(self.field.tileset))
        self.frame.root.mainloop()


    def getInsertion(self):
            for y in range(self.field.getHeight()):
                for x in range(self.field.getWidth()):
                    if self.field.field[x][y] == 0:
                        return (x,y)
                    
    def idToTile(self, ID):
        for tiles in self.field.tileset:
            if tiles[0].getID() == ID:
                tile = tiles[0]
        return tile
            
    

        
    def checkSolution(self):
        for sol in  self.uniqueSol:
            if sol == self.sizes:
               return False 
        return True
        
        
        
    def dfsAlgorithmSorted(self, visited_tiles, depth, maxDepth):

        self.steps = self.steps + 1
        
        iterations=100000
        if self.steps == iterations:
            print("Exceeded",iterations,"iterations")
            sys.exit()

        if self.field.solved():

         if self.checkSolution()==True:
                
                self.uniqueSol.append(self.sizes.copy()) 
                self.solution = self.solution + 1

                print("Solution number",self.solution, "at iteration", self.steps)


        if depth < maxDepth:

            
            #remove comment for bigger tiles to be placed first
            self.field.sortTilesetDecreasing()
            #remove comment for smaller tiles to be placed first
#            self.field.sortTilesetIncreasing()
            #remove comment for tiles to be sorted in random order
#            random.shuffle(self.field.tileset)
            
            
            it = iter(self.field.tileset)
            for tile in it:
                if (tile[0].getWidth() == self.lastTile.getWidth()) and (
                        tile[0].getHeight() == self.lastTile.getHeight()):
                    continue
                else:
                    if tile[1] == False:
                        if tile[0].getWidth != tile[0].getHeight:
                            tile[0].flip()
                        cord = self.getInsertion()
                        if self.field.tileFits(tile[0], cord[0], cord[1]):

                            self.field.placeTile(tile[0], cord[0], cord[1])
                            
                            
                            #remove comment to show a board and the precess of placing tiles
#                            self.frame.repaint(self.field)
                            
                            self.lastTile = Tile(30, 50, 50)
                            
                            self.sizes.append( (tile[0].width,tile[0].height) )
                            self.visited_tiles.append(tile[0].getID())

                            self.dfsAlgorithmSorted(self.visited_tiles, depth + 1, maxDepth)

                            lastID = tile[0].getID()
                            
                            self.sizes.pop()
                            self.visited_tiles.pop()
                            self.field.removeTile(tile[0])

                            self.lastTile = self.idToTile(lastID)
   
    
    
         
            




Assignment()
