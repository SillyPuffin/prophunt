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
Scale = max(screensize)// base_size[screensize.index(max(screensize))]
if Scale > 4:
    Scale = 4
window_size = (base_size[0]*Scale,base_size[1]*Scale)

#hello i like cheese

#main class
class Main():
    def __init__(self):
        self.GameState = 'menu'
        self.size = (window_size)
        self.quit = False
        self.scale = Scale
        self.guiscale = self.scale
        if exact:
            self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.image.load('graphics/font_sheet.png').convert()
        self.text = Text(self.guiscale,self.font,1)
        self.editor = None
        self.init_menu_groups()

    def regenMenus(self,activegroup):
        self.text = Text(self.guiscale,self.font,1)
        self.init_menu_groups()
        self.active_group = self.menu_groups[activegroup]

    def init_menu_groups(self):
        data = list(walk('levels'))[0][2]
        levels = []
        for name in data:
            with open(f'levels\{name}') as f:
                level_data = f.read()
            newbutton = Button((window_size[0],window_size[1]),(70,18),(0,100,200),self.text.render(name,1,False).image,self.guiscale,OpenLevel,level_data)
            levels.append(newbutton)
        
        box = self.text.render('he-llo my name is jeff and i like to eat cheese on wednesdays',1.25,(50,20))
        
        self.menu_groups = {
            #button(pos,size,colour,image,scale,func,arg)
            'main_group':Column((vec(window_size)/2),5,self.guiscale,'vertical',[
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('play',1,False).image,self.guiscale,switch_ButtonGroup,'play_group'),
                Button((base_size[0]/2,base_size[1]/2),(70,18),(0,100,200),self.text.render('level editor',1,False).image,self.guiscale,switch_ButtonGroup,'LevelSelect'),
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('settings',1,False).image,self.guiscale,switch_ButtonGroup,'settings'),
                Button((base_size[0]/2,base_size[1]/2+20),(70,18),(0,100,200),self.text.render('quit',1,False).image,self.guiscale,QuitGame)
                ]),
            'play_group':Column((100,135),5,self.guiscale,"vertical",[
                Button((base_size[0]/2,base_size[1]/2-30),(70,18),(0,100,200),self.text.render('join',1,False).image,self.guiscale),
                Button((base_size[0]/2,base_size[1]/2),(70,18),(0,100,200),self.text.render('host',1,False).image,self.guiscale),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group')
                ]),
            'LevelSelect':UiContainter([
                Button((window_size[0]-35*self.guiscale,window_size[1]-9*self.guiscale),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group'),
                Button((35*self.guiscale,window_size[1]-9*self.guiscale),(70,18),(0,100,200),self.text.render('new level',1,False).image,self.guiscale,CreateNewLevel),
                Column((window_size[0]/2,50),7,self.guiscale,'horizontal',[
                    *levels
                ])
                ]),
            'settings':Column((vec(window_size)/2),5,self.guiscale,'vertical',[
                Slider((0,0),(70,15),[(0,200,0),(255,0,0),(200,200,200)],self.guiscale,1,[1,4],self.guiscale),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group')
            ])
            
        }

        self.active_group = self.menu_groups['main_group']

    def CreateEditor(self,level=None):
        self.editor = None
        self.editor = Editor(self,self.screen,level)

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
                if self.guiscale != self.menu_groups['settings'].elements[0].barvalue:
                    self.guiscale = self.menu_groups['settings'].elements[0].barvalue
                    self.regenMenus(list(self.menu_groups.keys())[list(self.menu_groups.values()).index(self.active_group)])
                self.active_group.update(self.events,self.mouse,self)
            elif self.GameState == 'editor':
                self.editor.run(self,self.events)
                
            #drawing
            
            ####menu 
            if self.GameState == 'menu':
                self.screen.fill('red')
                self.active_group.draw(self.screen)

            #updating & framerate
            debug(int(self.clock.get_fps()),Scale)
            self.clock.tick(fps)
            pygame.display.update()

#running
if __name__ == '__main__':
    game = Main()
    game.run()
