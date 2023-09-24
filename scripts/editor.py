import pygame
import math,random
import time
from .properties import *


class Editor():
    def __init__(self,screen,level):        
        self.display = screen
        #init level
        if level: 
            print(level)
            self.LoadLevel(level)
        else:
            self.data = {}

    def LoadLevel(self,level):
        pass

    def run(self,game,events):
        self.display.fill((0,20,50))