import pygame
from os import walk
import json

def QuitGame(game):
    game.quit = True

def CreateNewLevel(game):
    game.GameState = 'editor'
    game.CreateEditor()

def OpenLevel(game,level):
    game.GameState = 'editor'
    game.CreateEditor(level)

def switch_ButtonGroup(game,group):
    game.active_group = game.menu_groups[group]
    game.active_group.update(game.events,game.mouse,game)

def quitEditor(game):
    game.GameState = 'menu'

def saveLevel(game,editor):
    #name for level
    levelData = editor.savedata
    levelnum = len(list(walk('levels'))[0][2]) + 1
    newjson = json.dumps(levelData)
    with open(f"levels/level {levelnum}.json","w") as f:
        json.dump(newjson, f)

