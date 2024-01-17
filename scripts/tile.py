import pygame
from pygame.math import Vector2 as vec


class LevelTile():
    def __init__(self,tileSize,data,pos,images,tiles={}):
        self.tileSize = tileSize
        self.total = ['0']
        #adddata
        self.AddData(data,pos,images,tiles)

    def AddData(self,data,pos,images,tiles={}):
        #data
        self.grid = pos
        self.pos = pos*self.tileSize
        self.data = data.copy()
        self.name = data['name']
        #rect
        self.rect = pygame.Rect(self.pos,(self.tileSize,self.tileSize))
        self.image = None
        #imaging
        if self.data['image']!= None and self.image == None:
            self.imageFromString(images)
        else:
            self.setImage(images,tiles)

    def imageFromString(self,images):
        self.image = pygame.Surface((self.tileSize,self.tileSize),pygame.SRCALPHA)
        self.total = self.data['image']
        self.image.blit(images[self.total[0]],(0,0))
        if len(self.total) > 1:
            for s in self.total[1]:
                self.image.blit(images[s],(0,0))

    def getData(self):
        data = self.data
        data['image'] = self.total
        return data

    def getNeighbour(self,tiles):
        getkey = lambda x: f'{int(x[0])}:{int(x[1])}'
        
        n = getkey([self.grid.x,self.grid.y-1])
        s = getkey([self.grid.x,self.grid.y+1])
        w = getkey([self.grid.x-1,self.grid.y])
        e = getkey([self.grid.x+1,self.grid.y])
        nw = getkey([self.grid.x-1,self.grid.y-1])
        ne = getkey([self.grid.x+1,self.grid.y-1])
        se = getkey([self.grid.x+1,self.grid.y+1])
        sw= getkey([self.grid.x-1,self.grid.y+1])

        neighbours = {
            'n':tiles[n] if n in tiles else None,
            's':tiles[s] if s in tiles else None,
            'w':tiles[w] if w in tiles else None,
            'e':tiles[e] if e in tiles else None,
            'nw':tiles[nw] if nw in tiles else None,
            'ne':tiles[ne] if ne in tiles else None,
            'se':tiles[se] if se in tiles else None,
            'sw':tiles[sw] if sw in tiles else None,
        }
        
        return neighbours
    
    def setImage(self,images,tiles):
        self.image = pygame.Surface((self.tileSize,self.tileSize),pygame.SRCALPHA)
        #fetch neignbours
        neighbours = self.getNeighbour(tiles)
        self.total = []
        #baseimage
        s = []
        if neighbours['n']:
            s.append('1')
        if neighbours['s']:
            s.append('3')
        if neighbours['w']:
            s.append('4')
        if neighbours['e']:
            s.append('2')
        #if empty
        if not s:
            s.append('0')
        s.sort()
        s = ''.join(s)
        self.total.append(s)
        #draw
        self.image.blit(images[s],(0,0))
        #corner
        if neighbours['n'] and neighbours['w'] and not neighbours['nw']:
            self.image.blit(images['5'],(0,0))
            self.total.append('5')
        if neighbours['n'] and neighbours['e'] and not neighbours['ne']:
            self.image.blit(images['6'],(0,0))
            self.total.append('6')
        if neighbours['s'] and neighbours['e'] and not neighbours['se']:
            self.image.blit(images['7'],(0,0))
            self.total.append('7')
        if neighbours['s'] and neighbours['w'] and not neighbours['sw']:
            self.image.blit(images['8'],(0,0))
            self.total.append('8')