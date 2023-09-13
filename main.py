import pygame; from pygame.locals import *
import random
from sys import exit
from os import walk

from scripts import *

pygame.init()

sinfo = pygame.display.Info()
screensize = (sinfo.current_w,sinfo.current_h)
remainder = max(screensize) % base_size[screensize.index(max(screensize))]
if remainder == 0:
    exact = True
else:
    exact = False
scale = max(screensize)// base_size[screensize.index(max(screensize))]
if scale > 4:
    scale = 4
window_size = (base_size[0]*scale,base_size[1]*scale)

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
        data = list(walk('levels'))[0][2]
        levels = []
        for name in data:
            newbutton = Button((base_size[0]-35,base_size[1]-9),(70,18),(0,100,200),self.text.render(name,1,False).image,self.scale,OpenLevel,f'{name}')
            levels.append(newbutton)
        
        self.menu_groups = {
            'main_group':Column((100,135),5,self.scale,'vertical',[
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('play',1,False).image,self.scale,switch_ButtonGroup,'play_group'),
                Button((base_size[0]/2,base_size[1]/2),(70,18),(0,100,200),self.text.render('level editor',1,False).image,self.scale,switch_ButtonGroup,'LevelSelect'),
                Button((base_size[0]/2,base_size[1]/2+20),(70,18),(0,100,200),self.text.render('quit',1,False).image,self.scale,QuitGame)
                ]),
            'play_group':Column((100,135),5,self.scale,"vertical",[
                Button((base_size[0]/2,base_size[1]/2-30),(70,18),(0,100,200),self.text.render('join',1,False).image,self.scale),
                Button((base_size[0]/2,base_size[1]/2),(70,18),(0,100,200),self.text.render('host',1,False).image,self.scale),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.scale,switch_ButtonGroup,'main_group')
                ]),
            'LevelSelect':UiContainter([
                Button((base_size[0]-35,base_size[1]-9),(70,18),(0,100,200),self.text.render('back',1,False).image,self.scale,switch_ButtonGroup,'main_group'),
                Button((35,base_size[1]-9),(70,18),(0,100,200),self.text.render('new level',1,False).image,self.scale,CreateNewLevel),
                Column((280,50),7,self.scale,'horizontal',[
                    *levels
                ])
                ])
            
        }

        self.active_group = self.menu_groups['main_group']

    def run(self):
        while True:
            self.events = pygame.event.get()
            if self.quit == True:
                pygame.quit()
                exit()
            for event in self.events:
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            

            self.mouse = pygame.mouse.get_pos()

            #updating
            ####menu
            if self.GameState == 'menu':
                self.active_group.update(self.events,self.mouse,self)
                
            #drawing
            self.screen.fill('red')
            ####menu 
            if self.GameState == 'menu':
                self.active_group.draw(self.screen)

            #updating & framerate
            debug(int(self.clock.get_fps()),scale)
            self.clock.tick(fps)
            pygame.display.update()

#running
if __name__ == '__main__':
    game = Main()
    game.run()
