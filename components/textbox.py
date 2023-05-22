import pygame

from utils.main import centered_x, centered_y, centered_x_y, font

bg_active = (175, 175, 175)
bg_passive = (200, 200, 200)

class TextBox:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()

        self.active = False
        self.color = (0, 0, 0)
        self.background = bg_passive

    def draw(self, text, x = 0, y = 0, label = ""):
        if(x == 0 and y == 0):
            self.rect.topleft = centered_x_y(self.screen, self.rect)
        elif(x == 0 and y != 0):
            self.rect.topleft = (centered_x(self.screen, self.rect), y)
        elif(x != 0 and y == 0):
            self.rect.topleft = (x, centered_y(self.screen, self.rect))
        else:
            self.rect.topleft = (x, y)

        self.surface.fill(self.background)

        self.input = font(20).render(text, True, (0, 0, 0))
        self.surface.blit(self.input, centered_x_y(self.surface, self.input.get_rect()))
        self.screen.blit(self.surface, self.rect)
