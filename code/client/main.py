import pygame; from pygame.locals import *
import random
import settings as st
from gui import *
from utils import debug
from sys import exit
from ButtonScripts import *

pygame.init()

sinfo = pygame.display.Info()
screensize = (sinfo.current_w,sinfo.current_h)
remainder = max(screensize) % st.base_size[screensize.index(max(screensize))]
if remainder == 0:
    exact = True
else:
    exact = False
scale = max(screensize)// st.base_size[screensize.index(max(screensize))]
window_size = (st.base_size[0]*scale,st.base_size[1]*scale)




#main class
class Main():
    def __init__(self):
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
                Button((window_size[0]/2,window_size[1]/2-50),(350,90),(0,100,200),self.text.render('play',1,False).image,self.switch_ButtonGroup,'play_group'),
                Button((window_size[0]/2,window_size[1]/2+50),(350,90),(0,100,200),self.text.render('level editor',1,False).image,self.switch_ButtonGroup,'LevelSelect'),
                Button((window_size[0]/2,window_size[1]/2+150),(350,90),(0,100,200),self.text.render('quit',1,False).image,QuitGame)
                ],
            'play_group':[
                Button((window_size[0]/2+100,window_size[1]/2),(200,70),(0,100,200),self.text.render('join',1,False).image),
                Button((window_size[0]/2-100,window_size[1]/2),(200,70),(0,100,200),self.text.render('host',1,False).image),
                Button((window_size[0]/2+100,window_size[1]/2+400),(200,70),(0,100,200),self.text.render('back',1,False).image,self.switch_ButtonGroup,'main_group')
                ],
            'LevelSelect':[
                Button((window_size[0]/2+100,window_size[1]/2+400),(200,70),(0,100,200),self.text.render('back',1,False).image,self.switch_ButtonGroup,'main_group')
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

            #menu
            for item in self.active_group:
                if item.type == 'button':
                    item.update(self.events,self.mouse,self)
                

            #drawing
            self.screen.fill('red')
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
