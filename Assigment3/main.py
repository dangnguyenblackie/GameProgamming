import os
import sys
import math
import random

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.button import Button
from scripts.menu import Menu
from scripts.gamestate import GameState

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WINDOW_TITLE = "Assignment 3"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set title
pygame.display.set_caption(WINDOW_TITLE)
# FROM HERE
'''MENU VALUES'''
startMenuButtonValues = None
pauseMenuButtonValues = None

# Menu background images
menuBackgroundImage = pygame.image.load("data/images/menu/menu.png").convert_alpha()
menuWeaponBackgroundImage = pygame.image.load("data/images/menu/weapon.png").convert_alpha()

# Menu weapon items
swordImage = pygame.image.load("data/images/menu/sword.png").convert_alpha()
gunImage = pygame.image.load("data/images/menu/gun.png").convert_alpha()
coinImage = pygame.image.load("data/images/menu/coin.png").convert_alpha()

# Button images
startButtonImage = pygame.image.load("data/images/buttons/start.png").convert_alpha()
pauseButtonImage = pygame.image.load("data/images/buttons/pause.png").convert_alpha()
exitButtonImage = pygame.image.load("data/images/buttons/exit.png").convert_alpha()
continueButtonImage = pygame.image.load("data/images/buttons/continue.png").convert_alpha()
storeButtonImage = pygame.image.load("data/images/buttons/store.png").convert_alpha()
backButtonImage = pygame.image.load("data/images/buttons/back.png").convert_alpha()

# Buttons      
startButton = Button(startButtonImage, padding=(0,150))
continueButton = Button(continueButtonImage, padding=(0,150))
exitButton = Button(exitButtonImage, padding=(0,30))
storeButton = Button(storeButtonImage, padding=(0,90))
backButton = Button(backButtonImage, padding=(0,-180))

# Store menu items
swordButton = Button(swordImage, padding=(-120, 0))
gunButton = Button(gunImage, padding=(120, 0))

'''Start Menu'''
startMenu = Menu(
buttons = [startButton, storeButton, exitButton],
menuBackground = menuBackgroundImage,
size = (320,240))

'''Pause Menu'''
pauseMenu = Menu(
buttons = [startButton, storeButton, exitButton],
menuBackground = menuBackgroundImage,
size = (320,240))

'''Weapon Menu'''
weaponMenu = Menu(
buttons = [backButton, swordButton, gunButton],
menuBackground = menuWeaponBackgroundImage,
size = (320,240))

'''GAME STATES'''
previosState = None
gameState = GameState.IS_START
clock = pygame.time.Clock()

# Menu
startMenu = startMenu
startMenu.setIsDisplay(True)

mouse = None
mousePosition = None

while gameState:
    mouse = 0
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = 1


    screen.fill((0, 0, 0))  # Xóa màn hình
    if gameState == GameState.IS_START:
        startMenuButtonValues = startMenu.draw(screen, mousePosition, mouse)['buttons']
        if startMenuButtonValues[0]: # Click Start button
            startMenu.setIsDisplay(False)
            previosState = gameState
            gameState =  GameState.IS_PLAY
        elif startMenuButtonValues[1]: # Click Store button
            startMenu.setIsDisplay(False)
            weaponMenu.setIsDisplay(True)
            previosState = gameState
            gameState =  GameState.IS_WEAPON
        elif startMenuButtonValues[2]: # Click exit button
            startMenu.setIsDisplay(False)
            previosState = gameState
            gameState = GameState.IS_EXIT
            

    elif gameState == GameState.IS_PAUSE:
        pauseMenu.draw(screen, mousePosition, mouse)['buttons']
    elif gameState == GameState.IS_WEAPON:
        weaponMenuButtonValues = weaponMenu.draw(screen, mousePosition, mouse)['buttons']
        if weaponMenuButtonValues[0]: # Click Back button
            weaponMenu.setIsDisplay(False)
            startMenu.setIsDisplay(True)
            previosState = gameState
            gameState =  GameState.IS_START

    pygame.display.flip() 
    clock.tick(60)
    
# Quit PyGame
pygame.mixer.music.stop()
pygame.quit()