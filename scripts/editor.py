import pygame
import math,random
import time
from properties import *


class Editor():
    def __init__(self,level):
        if level: 
            self.LoadLevel(level)
        else:
            self.data = {
                'blocks':[]
            }

    def LoadLevel(self,level):
        pass
