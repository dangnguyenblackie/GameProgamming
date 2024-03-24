import pygame
from scripts.utils import drawTextOnScreen
from scripts.config import *

class Slider:
  def __init__(self,
    position: tuple, size: tuple, initValue: float,
    minValue: int, maxValue: int, containerBackground=None,
    padding=(0,0)):

    self.leftPosition = position[0]
    self.topPosition = position[1]
    self.rightPosition = position[0] + size[0]

    self.size = size

    self.min = minValue
    self.max = maxValue

    self.initialValue = (self.rightPosition - self.leftPosition) * initValue

    self.containerRect = pygame.Rect(self.leftPosition, self.topPosition, self.size[0], self.size[1])
    self.buttonRect = pygame.Rect(self.leftPosition, self.topPosition, self.initialValue, self.size[1] - padding[1]//2)

    self.containerBackground = containerBackground
    self.padding = padding
    self.containerBackgroundRect = None

    if containerBackground:
      self.containerBackground = pygame.transform.scale(containerBackground, (self.containerRect.width + padding[0], self.containerRect.height + padding[1]))
      self.containerBackgroundRect = self.containerBackground.get_rect()
      self.containerBackgroundRect.center = self.containerRect.center

  def draw(self, surface, displayValue=False, font=None, textColor=TEXT_COLOR):
    if self.containerBackground:
      surface.blit(self.containerBackground, (self.containerBackgroundRect.x , self.containerBackgroundRect.y))
    else:
      pygame.draw.rect(surface, "white", self.containerRect)

    pygame.draw.rect(surface, "darkgrey", self.buttonRect)

    if displayValue:
      drawTextOnScreen(
        surface,
        str(self.getValue()),
        font,
        textColor,
        self.containerRect.right + SLIDER_FONT_SIZE,
        self.containerRect.top
      )

  def update(self, mousePosition, mouse):
    if self.containerRect.collidepoint(mousePosition) and mouse:
      # self.buttonRect.centerx = mousePosition[0]
      self.buttonRect = pygame.Rect(self.leftPosition, self.topPosition, mousePosition[0] - self.leftPosition, self.size[1] - self.padding[1]//2)

  def getValue(self, padding = (1,0)):
    valueRange = self.rightPosition - self.leftPosition - padding[0] - padding[1]
    buttonPosition = self.buttonRect.centerx - self.leftPosition

    # TODO: NORMALIZATION
    return int((buttonPosition/valueRange)*(self.max-self.min)*2+self.min)