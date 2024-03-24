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
from scripts.config import *

pygame.init()

WINDOW_TITLE = "Assignment 3"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set title
pygame.display.set_caption(WINDOW_TITLE)
# FROM HERE
'''MENU VALUES'''
startMenuButtonValues = None
pauseMenuButtonValues = None

# Load and scale menu background images
menuBackgroundImage = pygame.image.load("data/images/menu/menu.png").convert()
menuWeaponBackgroundImage = pygame.image.load("data/images/menu/weapon.png").convert()

# Load and scale menu weapon items
swordImage = pygame.image.load("data/images/menu/sword.png").convert()
gunImage = pygame.image.load("data/images/menu/gun.png").convert()
coinImage = pygame.image.load("data/images/menu/coin.png").convert()

# Load and scale button images
startButtonImage = pygame.image.load("data/images/buttons/start.png").convert()
pauseButtonImage = pygame.image.load("data/images/buttons/pause.png").convert()
exitButtonImage = pygame.image.load("data/images/buttons/exit.png").convert()
continueButtonImage = pygame.image.load("data/images/buttons/continue.png").convert()
storeButtonImage = pygame.image.load("data/images/buttons/store.png").convert()
backButtonImage = pygame.image.load("data/images/buttons/back.png").convert()

# Buttons
startButton = Button(startButtonImage, padding=(0,75))
continueButton = Button(continueButtonImage, padding=(0,75))
exitButton = Button(exitButtonImage, padding=(0,15))
storeButton = Button(storeButtonImage, padding=(0,45))
backButton = Button(backButtonImage, padding=(0,-90))

# Store menu items
swordButton = Button(swordImage, padding=(-60, 0))
gunButton = Button(gunImage, padding=(60, 0))

'''Start Menu'''
startMenu = Menu(
buttons = [startButton, storeButton, exitButton],
menuBackground = menuBackgroundImage,
size = (320,240))

'''Pause Menu'''
pauseMenu = Menu(
buttons = [startButton, exitButton],

size = (160,120))

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
            pauseMenu.setIsDisplay(True)
            previosState = gameState
            gameState =  GameState.IS_PAUSE
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