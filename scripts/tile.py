import pygame
from pygame.math import Vector2 as vec


class Tile():
    def __init__(self,tileSize,data,pos,images,tiles):
        self.tileSize = tileSize
        #adddata
        self.AddData(data,pos,images,tiles)

    def AddData(self,data,pos,images,tiles):
        #data
        self.grid = pos
        self.pos = pos*self.tileSize
        self.data = data
        self.name = data['name']
        #rect
        self.rect = pygame.Rect(self.pos,(self.tileSize,self.tileSize))
        self.image = pygame.Surface((self.tileSize,self.tileSize))#temporray
        self.image.fill('gold')
        #imaging
        self.setImage(images,tiles)

    def getData(self):
        return 0
    def getNeighbour(self,tiles):
        getkey = lambda x: f'{int(x.x)}:{int(x.y)}'
        getvec = lambda x: vec(int(x.split(':')[0]),int(x.split(':')[1]))
        
        n = getkey([self.grid.x,self.grid.y-1])
        s = getkey([self.grid.x,self.grid.y+1])
        w = getkey([self.grid.x-1,self.grid.y])
        e = getkey([self.grid.x+1,self.grid.y])
        nw = getkey([self.grid.x-1,self.grid.y-1])
        ne = getkey([self.grid.x+1,self.grid.y-1])
        se = getkey([self.grid.x+1,self.grid.y+1])
        sw= getkey([self.grid.x-1,self.grid.y+1])

        

        return None
    def setImage(self,images,tiles):
        neighbours = self.getNeighbour(tiles)
        