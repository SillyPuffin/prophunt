import pygame
import math,random
import time
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.key import get_pressed as keys
from pygame.image import load as load
from pygame.math import Vector2 as vec
from .properties import *
from .settings import *
from .utils import *
from .tile import Tile
from .gui import *


class Editor():
    def __init__(self,game,screen,level):
        #start
        self.images = game.images
        self.display = screen
        self.scale = game.scale
        self.guiscale = game.guiscale
        self.WINDOWSIZE = vec([base_size[0]*self.scale,base_size[1]*self.scale])
        self.origin = vec(self.WINDOWSIZE[0]//2,self.WINDOWSIZE[1]//2)

        #pan
        self.scroll_active = False
        self.scroll = vec()

        #text
        self.text = Text(self.guiscale,load('graphics/font_sheet.png'),1)

        #grid
        self.grid = pygame.Surface((self.WINDOWSIZE),pygame.SRCALPHA)
        self.mousestill = 0
        self.prev = vec()
        self.tile = vec()
        self.coords = None

        #blockplacement
        self.active_block = 'wood'
        self.tileSize = tile_size * self.scale

        #init level
        if level: 
            self.LoadLevel(level)
        else:
            self.savedata = {'offgrid':{},'grid':{}}
            self.rundata = {'offgrid':{},'grid':{}}

    def LoadLevel(self,level):
        pass

    def eventloop(self,events):
        pass

    def updateNeighbours(self,pos,images):
        getkey = lambda x: f'{int(x[0])}:{int(x[1])}'
        
        neighbours = [
        getkey([pos.x,pos.y-1]),
        getkey([pos.x,pos.y+1]),
        getkey([pos.x-1,pos.y]),
        getkey([pos.x+1,pos.y]),
        getkey([pos.x-1,pos.y-1]),
        getkey([pos.x+1,pos.y-1]),
        getkey([pos.x+1,pos.y+1]),
        getkey([pos.x-1,pos.y+1])
        ]
        for tile in neighbours:
            if tile in self.rundata['grid']:
                #regen savedata
                self.rundata['grid'][tile].setImage(images,self.rundata['grid'])
                self.savedata['grid'][tile] = self.rundata['grid'][tile].getData()
        
    def pan_input(self):
        if (pygame.MOUSEBUTTONDOWN,2) in self.inputEvents and mouse_buttons()[1]:
            self.scroll_active = True
            self.scroll = vec(mouse_pos()) - self.origin
        
        if not mouse_buttons()[1]:
            self.scroll_active = False

        if self.scroll_active:
            self.origin = vec(mouse_pos()) - self.scroll

    def BlockPlace(self):
        if mouse_buttons()[0] and self.active_block != None:
            pos = self.GetTilePos(mouse_pos())
            key = f'{int(pos.x)}:{int(pos.y)}'
            images = self.images.tile_sets[self.active_block]
            if key in self.rundata['grid']:
                if self.rundata['grid'][key].name != self.active_block:
                    self.rundata['grid'][key].AddData(blocks[self.active_block],pos,images,self.rundata['grid'])
                    self.updateNeighbours(pos,images)
                    self.savedata['grid'][key] = self.rundata['grid'][key].getData()
            else:
                new_tile = Tile(self.tileSize,blocks[self.active_block],pos,images,self.rundata['grid'])
                self.rundata['grid'][key] = new_tile
                self.updateNeighbours(pos,images)
                self.savedata['grid'][key] = new_tile.getData()
        
        if mouse_buttons()[2]:
            images = self.images.tile_sets[self.active_block]
            pos = self.GetTilePos(mouse_pos())
            key = f'{int(pos.x)}:{int(pos.y)}'
            if key in self.rundata['grid']:
                del self.rundata['grid'][key]
                del self.savedata['grid'][key]
                self.updateNeighbours(pos,images)

    def drawlines(self):
        cols = int(self.WINDOWSIZE[0] // scale(self.scale,tile_size))  
        rows = int(self.WINDOWSIZE[1] // scale(self.scale,tile_size))
        self.grid.fill((0,0,0,0))

        for col in range(cols+1):
            offset = self.origin[0] % scale(self.scale,tile_size)
            offset += scale(self.scale,col*tile_size)
            pygame.draw.line(self.grid,(189,147,249,100),(offset,0),(offset,self.WINDOWSIZE[1]))    
        
        for row in range(rows+1):
            offset = self.origin[1] % scale(self.scale,tile_size)
            offset += scale(self.scale,row*tile_size)
            pygame.draw.line(self.grid,(189,147,249,100),(0,offset),(self.WINDOWSIZE[0],offset))   
        
        self.display.blit(self.grid,(0,0))

    def GetTilePos(self,pos):
        pos = vec(pos) - self.origin
        x,y = int(pos.x//self.tileSize),int(pos.y//self.tileSize)
        return vec(x,y)

    def tiledetails(self):
        pos = vec(mouse_pos())
        self.tile = self.GetTilePos(pos)
        self.coords = self.text.render(f'{int(self.tile.x)}, {int(self.tile.y)}',1)

        if self.coords:
            self.display.blit(self.coords.image,(self.WINDOWSIZE[0]-self.coords.image.get_width()-1*self.scale,1*self.scale))

    def inputEvent(self,events):
        self.inputEvents = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.inputEvents.append((event.type,event.button))
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.inputEvents.append((event.type,event.button))

    def drawTiles(self):
        tiles = list(self.rundata['grid'].values())
        for tile in tiles:
            self.display.blit(tile.image,vec(tile.rect.topleft)+self.origin)

    def update(self,game,events):
        self.inputEvent(events)
        self.eventloop(events)

        #panning and grid
        self.pan_input()
        self.BlockPlace()

        #drawing
        self.display.fill((0,20,50))
        self.drawTiles()
        self.drawlines()
        pygame.draw.circle(self.display,(0,150,80),self.origin,scale(self.scale,2))
        self.tiledetails()