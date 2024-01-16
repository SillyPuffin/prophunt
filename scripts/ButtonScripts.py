import pygame

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