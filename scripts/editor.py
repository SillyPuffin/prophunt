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
from .gui import *


class Editor():
    def __init__(self,game,screen,level):
        self.display = screen
        self.scale = game.scale
        self.WINDOWSIZE = vec([base_size[0]*self.scale,base_size[1]*self.scale])
        self.origin = vec(self.WINDOWSIZE[0]//2,self.WINDOWSIZE[1]//2)

        #pan
        self.scroll_active = False
        self.scroll = vec()

        #text
        self.text = Text(self.scale,load('graphics/font_sheet.png'),1)

        #grid
        self.grid = pygame.Surface((self.WINDOWSIZE),pygame.SRCALPHA)
        self.mousestill = 0
        self.prev = vec()
        self.tile = vec()
        self.coords = None

        #init level
        if level: 
            self.LoadLevel(level)
        else:
            self.data = {}

    def LoadLevel(self,level):
        pass

    def eventloop(self,events):
        for event in events:
            self.pan_input(event)

    def pan_input(self,event=None):
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
                self.scroll_active = True
                self.scroll = vec(mouse_pos()) - self.origin
        
        if not mouse_buttons()[1]:
            self.scroll_active = False

        if self.scroll_active:
            self.origin = vec(mouse_pos()) - self.scroll

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
        ts = scale(self.scale,tile_size)
        x,y = int(pos.x//ts),int(pos.y//ts)
        return vec(x,y)

    def tiledetails(self):
        pos = vec(mouse_pos())
        self.tile = self.GetTilePos(pos)
        self.coords = self.text.render(f'{int(self.tile.x)}, {int(self.tile.y)}',0.5)

        if self.coords:
            self.display.blit(self.coords.image,(self.WINDOWSIZE[0]-self.coords.image.get_width(),0))

    def run(self,game,events):
        self.eventloop(events)
        
        #drawing
        self.display.fill((0,20,50))
        self.drawlines()
        pygame.draw.circle(self.display,(0,150,80),self.origin,scale(self.scale,2))
        self.tiledetails()