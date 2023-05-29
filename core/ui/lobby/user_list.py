import pygame
from core.ui.components.container import Container

from core.ui.components.text import Text

class UserList:
    def __init__(self, width: int, height: int, pos_x: int, pos_y: int, color: pygame.Color = (255, 100, 100)):
        self.container = Container(width, height, color, pos_x, pos_y)
        
        # self.font = pygame.font.SysFont("Roboto", 13)

        # self.width, self.height = width, height
        # self.pos_x, self.pos_y  = pos_x, pos_y
        # self.color              = color

    def render(self, surface: pygame.Surface, users):
        self.container.render(surface)