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
    game.menu_groups['levelSelect'].dictionary['levels'].removeItem(name)
    if name in game.levels.keys():
        del game.levels[name]
    closeLevelOptions(game)

def closeLevelOptions(game):
    game.active_group = game.menu_groups['levelSelect']
    deleteMenuGroup(game,[game.menu_groups, 'levelOption'])

def closeSaveOptions(game,editor):
    editor.active_group = editor.menu_groups['main']
    editor.active_key = 'main'
    deleteMenuGroup(game,[editor.menu_groups,'saveOption'])

def deleteMenuGroup(game,item):
    del item[0][item[1]]

def saveLevel(game,editor):
    #name for level
    names = list(walk('levels'))[0][2]
    names = list(map(lambda s: s[:-5],names))
    levelData = editor.savedata
    editor.saving = True
    with open(f"levels/{editor.name}.json","w") as f:
        json.dump(levelData, f,indent = 2)
    if editor.name not in names:
        game.menu_groups['levelSelect'].dictionary['levels'].createPages({editor.name:game.createLevelButton(f'{editor.name}')})
    else:
        game.menu_groups['levelSelect'].dictionary['levels'].dictionary[editor.name].arg = [levelData, editor.name]
