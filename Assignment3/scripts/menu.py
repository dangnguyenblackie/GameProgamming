# this is MENU class
from scripts.config import *
from scripts.slider import *
import pygame

class Menu:
    def __init__(self, buttons , sliders = [], images = [], imagesPosition = [], menuBackground=None, size = (500,500), xy = None):

        self.menuBackground = menuBackground
        # if menuBackground:
        #     self.menuBackground = pygame.transform.scale(menuBackground, (size[0]+50,size[1]+50))

        self.size = size
        if xy:
            self.x = xy[0]
            self.y = xy[1]
        elif menuBackground:
            #center align
            self.x = SCREEN_WIDTH // 2 - menuBackground.get_width() // 2
            self.y = SCREEN_HEIGHT // 2 - menuBackground.get_height() // 2
        else:
            #center align
            self.x = SCREEN_WIDTH // 2 - size[0] // 2
            self.y = SCREEN_HEIGHT // 2 - size[1] // 2

        self.isDisplay = False
        self.buttonsValue = [False] * len(buttons)
        self.buttons = buttons
        self.sliders = sliders
        self.images = images
        self.imagesPosition = imagesPosition

        self.slidersValue = None
        if sliders: self.slidersValue = [slider.getValue() for slider in sliders]

    # draw buttons, also get buttons value
    def draw(self, surface, mousePosition, mouse,backgroundColor = None, border = 0, sliderFont = None):
        if self.isDisplay:

            # draw background
            if self.menuBackground:
                surface.blit(self.menuBackground, (self.x, self.y))
            elif backgroundColor:
                pygame.draw.rect(surface, backgroundColor, (self.x, self.y, self.size[0], self.size[1]) , border)

            for i in range(len(self.images)):
                surface.blit(self.images[i], self.imagesPosition[i])

            for i in range(len(self.sliders)):
                self.sliders[i].update(mousePosition, mouse)
                self.sliders[i].draw(surface, displayValue=True, font=sliderFont)
                self.slidersValue[i] = self.sliders[i].getValue()

            for i in range(len(self.buttons)):
                self.buttonsValue[i] = self.buttons[i].draw(surface, mousePosition, mouse)


        return {
            "buttons": self.buttonsValue,
            "sliders": self.slidersValue,
        }

    def setButtonValue2False(self, buttonIndex = None, value=False):
        if buttonIndex:
            self.buttonsValue[buttonIndex] = value
        else:
            self.buttonsValue = [value] * len(self.buttons)

    def setIsDisplay(self, value):
        self.isDisplay = value

    def getIsDisplay(self):
        return self.isDisplay

    def setImage(self, image, index):
        self.images[index] = image