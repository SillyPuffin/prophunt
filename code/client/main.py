import pygame

pygame.init()


class Main():
    def __init__(self):
        self.size = (1080,1920)
        self.screen = pygame.display.set_mode()


    def run(self):
        pass

#running
if __name__ == 'main.py':
    game = Main()
    game.run()