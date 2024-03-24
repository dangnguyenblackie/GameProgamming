import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

WINDOW_TITLE = "ASSIGNMENT 3"
WINDOW_BACKGROUND = (0,30,0,155)

logo = [
  "█     █░ ▄▄▄      ▒███████▒ ",
  "▓█░ █ ░█░▒████▄    ▒ ▒ ▒ ▄▀░",
  "▒█░ █ ░█ ▒██  ▀█▄  ░ ▒ ▄▀▒░ ",
  "░█░ █ ░█ ░██▄▄▄▄██   ▄▀▒   ░",
  "░░██▒██▓  ▓█   ▓██▒▒███████▒",
  "░ ▓░▒ ▒   ▒▒   ▓▒█░░▒▒ ▓░▒░▒",
  "  ▒ ░ ░    ▒   ▒▒ ░░░▒ ▒ ░ ▒",
  "  ░   ░    ░   ▒   ░ ░ ░ ░ ░",
  "    ░          ░  ░  ░ ░    ",
  "                   ░        "
]

# Sounds
backgroundSoundPath = 'data/sound/music.wav'
backgroundSoundVolume = 0.3

# Set text font
INTRO_FONT = 'data/font/JetBrainsMonoNerdFontMono-Regular.ttf'
INTRO_FONT_SIZE = 20

BUTTON_FONT = 'data/font/BigBlueTermPlusNerdFont-Regular.ttf'
BUTTON_FONT_SIZE = 40
BUTTON_TEXT_COLOR = (219,243,162)

SLIDER_FONT = 'data/font/OpenDyslexicAltNerdFont-Bold.otf'
SLIDER_COLOR = (255,255,255)
SLIDER_FONT_SIZE = 20

TEXT_FONT = 'data/font/JetBrainsMonoNerdFontMono-Regular.ttf'
TEXT_COLOR = (255,255,255)
TEXT_FONT_SIZE = 25

# PLAY TIME IN TICK
FPS = 60
PLAY_TIME = 31

# Key binding
PAUSE_KEY = pygame.K_SPACE

