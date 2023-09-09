import pygame

def debug(s,scale,x=10,y=10):
    string = str(s)
    font = pygame.font.Font(None,10*scale)
    text = font.render(string,True,(255,255,255))
    screen = pygame.display.get_surface()
    screen.blit(text,(x,y))
