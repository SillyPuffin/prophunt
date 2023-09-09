import pygame; from pygame.locals import *
import random
from sys import exit

from scripts.gui import *
import scripts.settings as st
from scripts.utils import debug
from scripts.ButtonScripts import *

# import settings as st
# from gui import *
# from utils import debug
# from ButtonScripts import *

pygame.init()

sinfo = pygame.display.Info()
screensize = (sinfo.current_w,sinfo.current_h)
remainder = max(screensize) % st.base_size[screensize.index(max(screensize))]
if remainder == 0:
    exact = True
else:
    exact = False
scale = max(screensize)// st.base_size[screensize.index(max(screensize))]
if scale > 4:
    scale = 4
window_size = (st.base_size[0]*scale,st.base_size[1]*scale)

#main class
class Main():
    def __init__(self):
        self.GameState = 'menu'
        self.size = (window_size)
        self.quit = False
        self.scale = scale
        if exact:
            self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.image.load('graphics/font_sheet.png').convert()
        self.text = Text(scale,self.font,1)
        self.init_menu_groups()

    def init_menu_groups(self):
        self.menu_groups = {
            'main_group':[
                Button((st.base_size[0]/2,st.base_size[1]/2-20),(70,18),(0,100,200),self.text.render('play',1,False).image,self.scale,self.switch_ButtonGroup,'play_group'),
                Button((st.base_size[0]/2,st.base_size[1]/2),(70,18),(0,100,200),self.text.render('level editor',1,False).image,self.scale,self.switch_ButtonGroup,'LevelSelect'),
                Button((st.base_size[0]/2,st.base_size[1]/2+20),(70,18),(0,100,200),self.text.render('quit',1,False).image,self.scale,QuitGame)
                ],
            'play_group':[
                Button((st.base_size[0]/2,st.base_size[1]/2-30),(70,18),(0,100,200),self.text.render('join',1,False).image,self.scale),
                Button((st.base_size[0]/2,st.base_size[1]/2),(70,18),(0,100,200),self.text.render('host',1,False).image,self.scale),
                Button((st.base_size[0]/2,st.base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.scale,self.switch_ButtonGroup,'main_group')
                ],
            'LevelSelect':[
                Button((st.base_size[0]-35,st.base_size[1]-9),(70,18),(0,100,200),self.text.render('back',1,False).image,self.scale,self.switch_ButtonGroup,'main_group'),
                Button((35,st.base_size[1]-9),(70,18),(0,100,200),self.text.render('new level',1,False).image,self.scale,CreateNewLevel)
            ]

        }
        self.active_group = self.menu_groups['main_group'][:]

    def switch_ButtonGroup(self,group):
        self.active_group = self.menu_groups[group][:]
        for item in self.active_group:
            if item.type == 'button':
                item.update(self.events,self.mouse)

    def run(self):
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or self.quit == True:
                    pygame.quit()
                    exit()

            self.mouse = pygame.mouse.get_pos()

            #updating
            ####menu
            if self.GameState == 'menu':
                for item in self.active_group:
                    if item.type == 'button':
                        item.update(self.events,self.mouse,self)
                
            #drawing
            self.screen.fill('red')
            ####menu 
            if self.GameState == 'menu':
                for item in self.active_group:
                    self.screen.blit(item.image,item.rect)

            #updating & framerate
            debug(int(self.clock.get_fps()),scale)
            self.clock.tick(st.fps)
            pygame.display.update()

#running
if __name__ == '__main__':
    game = Main()
    game.run()
