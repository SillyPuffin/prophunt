import pygame; from pygame.locals import *
import random
import settings as st
from gui import *
from utils import debug
from sys import exit

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
        self.scale = scale
        if exact:
            self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.image.load('graphics/font_sheet.png').convert()
        self.text = Text(scale,self.font,1)
        self.button = Button((700,400),(300,80),(70,70,70),self.text.render('press for cheese',1).image,self.changebg)
        self.colour = (100,200,1)
        self.tbox = self.text.render('balls\n and cock',1,(100,0))
        self.tbox.rect.topleft = (600,200)
        self.boxes = []
    def changebg(self):
        newbox = self.text.render('cheese',1)
        newbox.rect.topleft = (random.randint(0,2000),random.randint(0,1000))
        self.boxes.append(newbox)
    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

            mouse = pygame.mouse.get_pos()
            self.button.update(events,mouse,[])

            self.screen.fill(self.colour)
            self.screen.blit(self.button.image,self.button.rect)
            for box in self.boxes:
                box.draw(self.screen)
            debug(int(self.clock.get_fps()),scale)
            self.clock.tick(st.fps)
            pygame.display.update()

#running
if __name__ == '__main__':
    game = Main()
    game.run()
