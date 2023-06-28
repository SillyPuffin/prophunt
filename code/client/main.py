import pygame; from pygame.locals import *
from sys import exit

pygame.init()

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