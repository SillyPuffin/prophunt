import pygame; from pygame.locals import *
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
        self.text = Text(self.scale,self.font,1)
        self.words = self.text.render("hello, how are you my good friend, have a g'day 1234 ?  aaaaaaaaaaaaaa aaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaa aaaaaaaa aaaaaaaaaaa aaaaaaaaaaaaaa aaaaaaaaaaaaa aaaaaaaaa aaaaaaaaaaaaaaaa aaaaaaa aaaaaaa!",1,(100,30),(255,200,3))
    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

            mouse = pygame.mouse.get_pos()

            self.screen.fill(0)

            # debug(int(self.clock.get_fps()),scale)
            self.words.update(events,mouse,self.screen)
            # self.words.draw(self.screen)
            pygame.draw.rect(self.screen,(0,255,0),self.words.rect,1)

            self.clock.tick(st.fps)
            pygame.display.update()

#running
if __name__ == '__main__':
    game = Main()
    game.run()
