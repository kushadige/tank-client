import pygame

from utils.main import draw_text, centered_x, centered_y, centered_x_y, font
from constants import *

class Button:
    def __init__(self, screen, image, scale_x = 1, scale_y = 1, text = ""):
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale_x, self.scale_y = scale_x, scale_y
        self.screen = screen
        self.surface = pygame.transform.scale(image, (int(self.width * self.scale_x), int(self.height * self.scale_y)))
        self.rect = self.surface.get_rect()
        self.text = text

    def update(self, image):
        self.surface = pygame.transform.scale(image, (int(self.width * self.scale_x), int(self.height * self.scale_y)))

    def draw(self, x = 0, y = 0, font_size = 24):
        if(x == 0 and y == 0):
            self.rect.topleft = centered_x_y(self.screen, self.rect)
        elif(x == 0 and y != 0):
            self.rect.topleft = (centered_x(self.screen, self.rect), y)
        elif(x != 0 and y == 0):
            self.rect.topleft = (x, centered_y(self.screen, self.rect))
        else:
            self.rect.topleft = (x, y)

        draw_text(self.surface, self.text, font(font_size), BLACK)
        self.screen.blit(self.surface, self.rect)