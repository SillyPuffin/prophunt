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
from .tile import LevelTile
from .gui import *
from .ButtonScripts import *

import copy

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

        #menu
        self.menu = False
        self.saveindicator = self.text.render('saving...', 1, (0,200,0))
        self.saveindicator.rect.bottomleft = (2*self.scale,self.WINDOWSIZE[1]-2*self.scale)
        self.saving = False
        self.saved = None
        self.createMenu()

        #grid
        self.grid = pygame.Surface((self.WINDOWSIZE),pygame.SRCALPHA)
        self.mousestill = 0
        # self.prev = vec()
        self.tile = vec()
        self.coords = None

        #blockplacement
        self.active_block = 'wood'
        self.tileSize = tile_size * self.scale

        #init level
        if level != None: 
            self.LoadLevel(copy.deepcopy(level[0]))
            self.name = level[1]
        else:
            self.name = self.getName()
            self.savedata = {'offgrid':{},'grid':{}}
            self.rundata = {'offgrid':{},'grid':{}}

    def getName(self):
        names = list(walk('levels'))[0][2]
        names = list(map(lambda s: s[:-5],names))
        levelnum = len(names) + 1
        name = f'level {levelnum}'
        if name in names:
            testnum = 1
            testname = f'{name} ({testnum})'
            while testname in names:
                testnum += 1
                testname = f'{name} ({testnum})'
            name = testname

        return name

    def createMenu(self):
        self.menu_groups = {
            'main':Column(self.WINDOWSIZE/2,5,self.scale,'vertical','main',{
                'saveexit':Button((0,0),(80,18),(0,100,200),self.text.render('save and exit',1).image,self.guiscale,self.saveOptions,True),
                'save':Button((0,0),(80,18),(0,100,200),self.text.render('save',1).image,self.guiscale, self.saveOptions, False),
                'exit':Button((0,0),(80,18),(0,100,200),self.text.render('exit',1).image,self.guiscale,quitEditor)
                
        })
        }
        self.active_group = self.menu_groups['main']
        self.active_key = 'main'
        self.makeMenuBack()

    def makeMenuBack(self):
        self.blanks = {}
        for key in self.menu_groups:
            blanksize = vec(self.menu_groups[key].rect.size)
            blanksize[0] += 10* self.guiscale; blanksize[1] += 10 * self.guiscale
            blankrect = pygame.Rect((0,0),(blanksize))
            blankrect.center = self.WINDOWSIZE/2
            blanksurf = pygame.Surface(blanksize,pygame.SRCALPHA)
            pygame.draw.rect(blanksurf,(0,0,0,100),((0,0),(blanksize)))
            self.blanks[key] = (blanksurf,blankrect)

    #button script
    def saveOptions(self,game,doQuit):
        temp = {
            'confirm':None,
            'cancel':Button((0,0),(70,18),(0,100,200),self.text.render('cancel').image,self.guiscale,closeSaveOptions,self)
        }
        #CHECKING IF SAVE AND QUIT OR JUST SAVE
        if doQuit:
            temp['confirm'] = Button((0,0),(70,18),(0,100,200),self.text.render('confirm').image,self.guiscale,saveQuitEditor, self)
        else:
            temp['confirm'] = Button((0,0),(70,18),(0,100,200),self.text.render('confirm').image,self.guiscale, saveLevel, self)
        
        buttons = {
        'rename':Button((0,0),(145,18),(0,100,200),self.text.render(self.name).image,self.guiscale),
        'column':Column((0,0),5,self.guiscale,'horizontal','yes/no',temp)
        }

        self.menu_groups['saveOption'] = Column(vec(self.WINDOWSIZE)/2,5,self.guiscale,'vertical','saveOption',buttons)
        buttons['column'].centerElements()

        self.active_group = self.menu_groups['saveOption']
        self.active_key = 'saveOption'
        self.makeMenuBack()

    def LoadLevel(self,level):
        self.savedata = level
        self.rundata = {'offgrid':{},'grid':{}}
        for key in self.savedata['grid']:
            pos = vec(list(map(lambda x: int(x),key.split(':'))))
            data = self.savedata['grid'][key]
            images = self.images.tile_sets[data['name']]
            newtile = LevelTile(self.tileSize,data,pos,images)
            self.rundata['grid'][key] = newtile

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
                _images = images[self.rundata['grid'][tile].data['name']]
                self.rundata['grid'][tile].setImage(_images,self.rundata['grid'])
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
        if mouse_buttons()[0] and self.active_block != None and self.menu == False:
            pos = self.GetTilePos(mouse_pos())
            key = f'{int(pos.x)}:{int(pos.y)}'
            images = self.images.tile_sets[self.active_block]#tileset
            if key in self.rundata['grid']:
                if self.rundata['grid'][key].name != self.active_block:
                    self.rundata['grid'][key].AddData(blocks[self.active_block],pos,images,self.rundata['grid'])
                    self.updateNeighbours(pos,self.images.tile_sets)
                    self.savedata['grid'][key] = self.rundata['grid'][key].getData()
            else:
                new_tile = LevelTile(self.tileSize,blocks[self.active_block],pos,images,self.rundata['grid'])
                self.rundata['grid'][key] = new_tile
                self.updateNeighbours(pos,self.images.tile_sets)
                self.savedata['grid'][key] = new_tile.getData()
            
        if mouse_buttons()[2] and self.menu == False:
            images = self.images.tile_sets[self.active_block]
            pos = self.GetTilePos(mouse_pos())
            key = f'{int(pos.x)}:{int(pos.y)}'
            if key in self.rundata['grid']:
                del self.rundata['grid'][key]
                del self.savedata['grid'][key]
                self.updateNeighbours(pos,self.images.tile_sets)

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
                self.inputEvents.append((event.type,event.key))

    def drawTiles(self):
        tiles = list(self.rundata['grid'].values())
        for tile in tiles:
            self.display.blit(tile.image,vec(tile.rect.topleft)+self.origin)

    def drawMenu(self):
        if self.menu:
            self.display.blit(self.blanks[self.active_key][0],self.blanks[self.active_key][1])
            self.active_group.draw(self.display)

        if self.saving :
            if self.saved == None:
                self.saved = time.time()
            current = time.time()
            if (current - self.saved) >= 1:
                self.saving = False
                self.saved = None

        if self.saving:
            self.saveindicator.draw(self.display)
    
    def updateMenu(self,events,mouse,game):
        if (pygame.KEYUP,pygame.K_ESCAPE) in self.inputEvents:
            self.menu = not self.menu
        if self.menu:
            self.active_group.update(events,mouse,game)

    def update(self,game,events):
        self.inputEvent(events)

        #updating
        self.updateMenu(events,game.mouse,game)
        
        #panning and grid
        self.pan_input()
        self.BlockPlace()

        #drawing
        self.display.fill((0,20,50))
        self.drawTiles()
        self.drawlines()
        pygame.draw.circle(self.display,(0,150,80),self.origin,scale(self.scale,2))
        self.tiledetails()
        self.drawMenu()
