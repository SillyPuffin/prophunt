import pygame

def debug(s,Scale,x=10,y=10):
    string = str(s)
    font = pygame.font.Font(None,10*Scale)
    text = font.render(string,True,(255,255,255))
    screen = pygame.display.get_surface()
    screen.blit(text,(x,y))

def scale(scale,value):
    if type(value) == tuple:
        t = (value[0]*scale,value[1]*scale)
        return t
    elif type(value) == list:
        l = []
        for num in value:
            l.append(num*scale)
        return l
    else :
        return value*scale
