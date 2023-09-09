import pygame

def QuitGame(game):
    game.quit = True

def CreateNewLevel(game):
    game.GameState = 'editor'