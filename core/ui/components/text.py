import pygame

class Text:
    def __init__(self, text: str, size: int, pos_x: int, pos_y: int, color: pygame.Color, justifyCenter: bool = True, alignCenter: bool = True):
        self.font   = pygame.font.Font("assets/font/Pogo-0W6WX.ttf", size)
        self.color  = color
        self.text   = self.font.render(text, True, self.color)
        self.pos_x, self.pos_y = pos_x, pos_y

        self.justifyCenter  = justifyCenter
        self.alignCenter    = alignCenter
        
    def change_text(self, new_text: str, new_color: pygame.Color = None):
        if new_color: self.text = self.font.render(new_text, True, new_color)
        else: self.text = self.font.render(new_text, True, self.color)

    def render(self, surface: pygame.Surface):
        if self.justifyCenter: self.pos_x = (surface.get_width() - self.text.get_width()) / 2
        if self.alignCenter: self.pos_y = (surface.get_height() - self.text.get_height()) / 2
        surface.blit(self.text, (self.pos_x, self.pos_y))