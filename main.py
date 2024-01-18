import pygame; from pygame.locals import *
import random
from sys import exit
from os import walk

from scripts import *

#possibly add solution for ui to scale instead of regening

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
        self.images = Images(Scale)
        self.clock = pygame.time.Clock()
        self.font = pygame.image.load('graphics/font_sheet.png').convert()
        self.text = Text(self.guiscale,self.font,1)
        self.editor = None
        self.init_menu_groups()

    def regenMenus(self,activegroup):
        self.text = Text(self.guiscale,self.font,1)
        self.init_menu_groups()
        self.active_group = self.menu_groups[activegroup]

    def createLevelButtons(self):
        data = list(walk('levels'))[0][2]
        self.levels = []
        for name in data:
            newbutton = self.createLevelButton(name)
            self.levels.append(newbutton)

    def createLevelButton(self,name):
        with open(f'levels/{name}') as f:
                level_dict = json.load(f)
        newname = name.lower()
        newname = newname[:-5]
        level_data = [level_dict,newname]
        newbutton = Button((window_size[0],window_size[1]),(70,18),(0,100,200),self.text.render(newname,1,False).image,self.guiscale,self.levelOptions,level_data)

        return newbutton

    def levelOptions(self,game,data):
        self.menu_groups['levelOption'] = Column(vec(window_size)/2,5,self.guiscale,'vertical','levelOption',{
            'rename':Button((0,0),(70,18),(0,100,200),self.text.render('rename').image,self.guiscale),
            'edit':Button((0,0),(70,18),(0,100,200),self.text.render('edit').image,self.guiscale,OpenLevel,data),
            'delete':Button((0,0),(70,18),(0,100,200),self.text.render('delete').image,self.guiscale,deleteLevel,data[1]),
            'back':Button((0,0),(70,18),(0,100,200),self.text.render('back').image,self.guiscale,closeLevelOptions)
        })
        self.active_group = self.menu_groups['levelOption']

    def init_menu_groups(self):
        self.createLevelButtons()
        self.menu_groups = {
            #button(pos,size,colour,image,scale,func,arg)
            'main_group':Column((vec(window_size)/2),5,self.guiscale,'vertical','main_group',[
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('play',1,False).image,self.guiscale,switch_ButtonGroup,'play_group'),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('level editor',1,False).image,self.guiscale,switch_ButtonGroup,'levelSelect'),
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('settings',1,False).image,self.guiscale,switch_ButtonGroup,'settings'),
                Button((base_size[0]/2,base_size[1]/2+20),(70,18),(0,100,200),self.text.render('quit',1,False).image,self.guiscale,QuitGame)
                ]),
            'play_group':Column(scale(self.scale,(100,135)),5,self.guiscale,"vertical",'play_group',[
                Button((base_size[0]/2,base_size[1]/2-30),(70,18),(0,100,200),self.text.render('join',1,False).image,self.guiscale),
                Button((base_size[0]/2,base_size[1]/2),(70,18),(0,100,200),self.text.render('host',1,False).image,self.guiscale),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group')
                ]),
            'levelSelect':UiContainter("levelSelect",[
                Button((window_size[0]-35*self.guiscale,window_size[1]-9*self.guiscale),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group'),
                Button((35*self.guiscale,window_size[1]-9*self.guiscale),(70,18),(0,100,200),self.text.render('new level',1,False).image,self.guiscale,CreateNewLevel),
                Grid((vec(window_size)/2),5,self.guiscale,self.scale,self.text,(400,200),'fixed','levelselect',self.levels)
                ]),
            'settings':Column((vec(window_size)/2),5,self.guiscale,'vertical',"settings",{
                'gui':Slider((0,0),(70,15),[(0,100,200),(0,75,200),(0,120,200)],self.guiscale,1,[1,8],self.guiscale),
                'backbutton':Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group')
                })
            
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
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            

            self.mouse = pygame.mouse.get_pos()
            #updating
            ####menu
            if self.GameState == 'menu':
                #menu
                if self.active_group.name == 'settings':
                    if self.guiscale != self.active_group.dictionary['gui'].barvalue:
                        value = self.active_group.dictionary['gui'].offset // self.guiscale
                        self.guiscale = self.active_group.dictionary['gui'].barvalue
                        self.regenMenus(list(self.menu_groups.keys())[list(self.menu_groups.values()).index(self.active_group)])
                        self.active_group.dictionary['gui'].offset = value * self.guiscale
                self.active_group.update(self.events,self.mouse,self)

            elif self.GameState == 'editor':
                self.editor.update(self,self.events)
                
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
