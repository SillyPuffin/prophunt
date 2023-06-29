import pygame; from pygame.locals import *
import settings as st
from sys import exit
#hey
pygame.init()

sinfo = pygame.display.Info()
screensize = (sinfo.current_w,sinfo.current_w)

scale = max(screensize)// st.base_size[screensize.index(max(screensize))]
print(scale)


#main class
class Main():
    def __init__(self):
        self.size = (1920,1080)
        self.screen = pygame.display.set_mode(self.size)


    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            pygame.display.update()

#running
if __name__ == '__main__':
    game = Main()
    game.run()
