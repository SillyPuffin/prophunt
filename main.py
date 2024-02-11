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
# if Scale > 4:
#     Scale = 4
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

        self.word = self.text.render('happen     \n  in',1,(0,255,0),50)

        self.init_menu_groups()
        #self.word.rect.topleft = (0,0)

    def regenMenus(self,activegroup):
        self.text = Text(self.guiscale,self.font,1)
        self.init_menu_groups()
        self.active_group = self.menu_groups[activegroup]

    def createLevelButtons(self):
        data = list(walk('levels'))[0][2]
        self.levels = {}
        for name in data:
            newname = name.lower()
            newname = newname[:-5]
            newbutton = self.createLevelButton(newname)
            self.levels[newname] = newbutton

    def createLevelButton(self,name):
        with open(f'levels/{name}.json') as f:
                level_dict = json.load(f)
        level_data = [level_dict,name]
        newbutton = Button((window_size[0],window_size[1]),(90,18),(0,100,200),self.text.render(name,1,False).image,self.guiscale,self.levelOptions,level_data)

        return newbutton

    def levelOptions(self,game,data):
        self.menu_groups['levelOption'] = Column(vec(window_size)/2,5,self.guiscale,'vertical','levelOption',{
            'rename':TextBox((0,0),(70,18),2,(0,100,150),(0,100,200),self.guiscale,self,'helo',False),
            'load':Button((0,0),(70,18),(0,100,200),self.text.render('load').image,self.guiscale,OpenLevel,data),
            'delete':Button((0,0),(70,18),(0,100,200),self.text.render('delete').image,self.guiscale,deleteLevel,data[1]),
            'back':Button((0,0),(70,18),(0,100,200),self.text.render('back').image,self.guiscale,closeLevelOptions)
        })
        self.active_group = self.menu_groups['levelOption']

    def init_menu_groups(self):
        self.createLevelButtons()
        self.menu_groups = {
            #button(pos,size,colour,image,scale,func,arg)
            'main_group':Column((vec(window_size)/2),5,self.guiscale,'vertical','main_group',[
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('play',1).image,self.guiscale,switch_ButtonGroup,'play_group'),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('level editor',1,False).image,self.guiscale,switch_ButtonGroup,'levelSelect'),
                Button((base_size[0]/2,base_size[1]/2-20),(70,18),(0,100,200),self.text.render('settings',1,False).image,self.guiscale,switch_ButtonGroup,'settings'),
                Button((base_size[0]/2,base_size[1]/2+20),(70,18),(0,100,200),self.text.render('quit',1,False).image,self.guiscale,QuitGame)
                ]),
            'play_group':Column(scale(self.scale,(100,135)),5,self.guiscale,"vertical",'play_group',[
                Button((base_size[0]/2,base_size[1]/2-30),(70,18),(0,100,200),self.text.render('join',1,False).image,self.guiscale),
                Button((base_size[0]/2,base_size[1]/2),(70,18),(0,100,200),self.text.render('host',1,False).image,self.guiscale),
                Button((base_size[0]/2,base_size[1]/2+40),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group')
                ]),
            'levelSelect':UiContainter("levelSelect",{
                'back':Button((window_size[0]-35*self.guiscale,window_size[1]-9*self.guiscale),(70,18),(0,100,200),self.text.render('back',1,False).image,self.guiscale,switch_ButtonGroup,'main_group'),
                'new':Button((35*self.guiscale,window_size[1]-9*self.guiscale),(70,18),(0,100,200),self.text.render('new level',1,False).image,self.guiscale,CreateNewLevel),
                'levels':Grid((vec(window_size)/2),5,self.guiscale,self.scale,self.text,(400,200),'fixed','levelselect',self.levels)
            }),
            'settings':Column((vec(window_size)/2),5,self.guiscale,'vertical',"settings",{
                'gui':Slider((0,0),(70,15),[(0,100,200),(0,75,200),(0,120,200)],self.guiscale,1,[1,8],resizeMenus,self.guiscale),
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
                self.active_group.update(self.events,self.mouse,self)

            elif self.GameState == 'editor':
                self.editor.update(self,self.events)
                
            #drawing
            
            ####menu 
            if self.GameState == 'menu':
                self.screen.fill('red')
                self.active_group.draw(self.screen)
                self.word.draw(self.screen)
                # pygame.draw.line(self.screen,(255,255,255),self.word.positions[0][11][1],(self.word.positions[0][11][1][0],self.word.positions[0][11][1][1]+60))

            #updating & framerate
            debug(int(self.clock.get_fps()),Scale)
            self.clock.tick(fps)
            pygame.display.update()


#running
if __name__ == '__main__':
    game = Main()
    game.run()
