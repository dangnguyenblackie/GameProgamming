# This is button class

import pygame

from scripts.config import *

class Button:
    def __init__(self, image, scale = 1, xy = None, padding=None, background = None):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))

        self.background = background

        if background:
            self.background = pygame.transform.scale(background,
                                    (   int(background.get_width()*scale),
                                        int(background.get_height()*scale)
                                    )
                                )
            self.rectangle = self.background.get_rect()

        else:
            self.rectangle = self.image.get_rect()

        if xy:
            self.rectangle.topleft = (xy[0],xy[1])
        elif padding:
            if background:
                self.rectangle.topleft = (
                    SCREEN_WIDTH//2 - int(background.get_width()*scale)//2 - padding[0],
                    SCREEN_HEIGHT//2 - int(background.get_height()*scale)//2 - padding[1]
                )
            else:
                self.rectangle.topleft = (
                    SCREEN_WIDTH//2 - int(width*scale)//2 - padding[0],
                    SCREEN_HEIGHT//2 - int(height*scale)//2 - padding[1]
                )
        else:
            self.rectangle.topleft = (0,0)

        # set image center in background
        if background:
            self.imageRect = self.image.get_rect()
            self.imageRect.center = self.rectangle.center

        self.clicked = False

    def draw(self, surface, mousePosition, mouse):
        action = False

        if self.rectangle.collidepoint(mousePosition):
            if mouse == 1 and self.clicked== False:
                self.clicked = True
                action = True

        if mouse == 0:
            self.clicked = False

        if self.background:
            surface.blit(self.background, (self.rectangle.x, self.rectangle.y))
            surface.blit(self.image, self.imageRect)
        else:
            surface.blit(self.image, (self.rectangle.x, self.rectangle.y))
        return action

