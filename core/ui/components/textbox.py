import pygame
from core.ui.colors import BLACK
from util.image import slice_and_assemble

class TextBox:
    def __init__(self, pos_x: int = 0, pos_y: int = 0, width: int = 0, height: int = 0, justifyCenter: bool = False, alignCenter: bool = False, callback = None):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

        self.font = pygame.font.Font("assets/font/Pogo-0W6WX.ttf", 25)
        self.inpt = ""
        self.text = self.font.render(self.inpt, True, BLACK)

        self.backgrounds = slice_and_assemble("assets/gray_slice.png", (24, 24), (8, 8), (width, height))
        self.current_bg = 0

        self.justifyCenter  = justifyCenter
        self.alignCenter    = alignCenter

        self.active         = False
        self.callback       = callback


    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    

    def on_typing(self, txt: str):
        self.inpt += txt
        self.text = self.font.render(self.inpt, True, BLACK)
        self.callback(self.inpt)
    
    def on_erasing(self):
        self.inpt = self.inpt[:-1]
        self.text = self.font.render(self.inpt, True, BLACK)
        self.callback(self.inpt)

    def erase_all(self):
        self.inpt = ""
        self.text = self.font.render(self.inpt, True, BLACK)
        self.callback(self.inpt)

    def on_mouse_over(self):
        self.current_bg = 1
    def on_mouse_off(self):
        if not self.active:
            self.current_bg = 0
    def on_mouse_press(self):
        self.current_bg = 1
    def on_mouse_release(self):
        self.current_bg = 1

    def render(self, surface: pygame.Surface):
        if self.justifyCenter: self.rect.x = (surface.get_width() - self.rect.width) / 2
        if self.alignCenter: self.rect.y = (surface.get_height() - self.rect.width) / 2
        
        surface.blit(self.backgrounds[self.current_bg], self.rect)

        pos = (
            self.rect.x + (self.rect.width - self.text.get_width()) / 2,
            self.rect.y + (self.rect.height - self.text.get_height()) / 2
        )

        surface.blit(self.text, pos)