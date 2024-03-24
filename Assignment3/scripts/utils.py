import os

import pygame
from scripts.config import *

BASE_IMG_PATH = 'data/images/'

def drawTextOnScreen(surface, text, font, textColor, x, y):

    img = font.render(text, True, textColor)
    surface.blit(img, (x,y))

def convertGameTime2Minute(time):
    minute = (time // FPS) // 60
    second = (time // FPS) - 60 * minute
    return "{:02d}:{:02d}".format(minute, second)

def load_sprite_sheet(file_path, rows, cols, scale=1):
    sheet = pygame.image.load(file_path).convert_alpha()
    sheet_rect = sheet.get_rect()
    frame_width = sheet_rect.width // cols
    frame_height = sheet_rect.height // rows

    scaled_frames = []
    for row in range(rows):
        for col in range(cols):
            frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frame = sheet.subsurface(frame_rect)
            scaled_frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
            scaled_frames.append(scaled_frame)

    return scaled_frames

def load_frames_from_sprite_sheet(file_path, size, rowIndex, numberOfCol=0, scale=1):
    sheet = pygame.image.load(file_path).convert_alpha()
    sheet_rect = sheet.get_rect()
    frame_width = size[0]
    frame_height = size[1]

    scaled_frames = []

    for col in range(numberOfCol):
        frame_rect = pygame.Rect(col * frame_width, rowIndex * frame_height, frame_width, frame_height)
        frame = sheet.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
        scaled_frames.append(scaled_frame)

    return scaled_frames

def fillImageColor(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color

    # Create a new surface with the same size and transparency
    newSurface = pygame.Surface((w, h), pygame.SRCALPHA)

    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            newSurface.set_at((x, y), pygame.Color(r, g, b, a))

    return newSurface

def getStars(points, acticeStar, unActiveStar):
    if points == 0:
        return 3*[unActiveStar]

    if points == 1:
        return [acticeStar] + 2*[unActiveStar]

    if points == 2:
        return 2*[acticeStar] + [unActiveStar]

    return 3*[acticeStar]

def calculate_distance(pos1, pos2):
    return (pos1[0]-pos2[0])*(pos1[0]-pos2[0]) + (pos1[1] - pos2[1])*(pos1[1] - pos2[1])

def myFunc(e):
    return e.split('.')[0]

def load_image(path, scale = 1):
    img = pygame.transform.scale_by(pygame.image.load(BASE_IMG_PATH + path).convert(), scale)
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path, scale = 1):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, scale = scale))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

class Timer:
    def __init__(self, time):
        self.time = time*FPS
        self.currentTime = time*FPS

    def reset(self):
        self.currentTime = self.time

    def run(self):
        self.currentTime -= 1

    def getFlag(self):
        self.run()
        if self.currentTime <= 0:
            self.reset()
            return True
        return False
