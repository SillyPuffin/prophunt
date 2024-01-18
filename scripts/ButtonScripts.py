import pygame
import os
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
    closeLevelOptions(game)

def switch_ButtonGroup(game,group):
    game.active_group = game.menu_groups[group]
    game.active_group.update(game.events,game.mouse,game)

def quitEditor(game):
    game.GameState = 'menu'
    game.editor = None
    
def saveQuitEditor(game,editor):
    saveLevel(game,editor)
    quitEditor(game)

def deleteLevel(game,name):
    os.remove(f'levels/{name}.json')
    game.createLevelButtons()
    game.menu_groups['levelSelect'].elements[2].elements = []
    game.menu_groups['levelSelect'].elements[2].createPages(game.levels)
    closeLevelOptions(game)

def closeLevelOptions(game):
    game.active_group = game.menu_groups['levelSelect']
    del game.menu_groups['levelOption']

def saveLevel(game,editor):
    #name for level
    names = list(walk('levels'))[0][2]
    names = list(map(lambda s: s[:-5],names))
    levelData = editor.savedata
    with open(f"levels/{editor.name}.json","w") as f:
        json.dump(levelData, f)
    if editor.name not in names:
        game.menu_groups['levelSelect'].elements[2].createPages(game.createLevelButton(f'{editor.name}.json'))
   