import pygame
from core.ui.colors import WHITE
from util.image import slice_and_assemble

class Button:
    def __init__(self, text: str, callback, pos_x: int = 0, pos_y: int = 0, width: int = 0, height: int = 0, justifyCenter: bool = False, alignCenter: bool = False, color: str = "gray"):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.callback = callback

        self.font = pygame.font.Font("assets/font/Pogo-0W6WX.ttf", 25)
        self.text = self.font.render(text, True, WHITE)

        self.backgrounds = slice_and_assemble("assets/button.png", (24, 24), (8, 8), (width, height))
        if color == "yellow": self.backgrounds = slice_and_assemble("assets/yellow_slice.png", (24, 24), (8, 8), (width, height))
        if color == "blue": self.backgrounds = slice_and_assemble("assets/blue_slice.png", (24, 24), (8, 8), (width, height))
        if color == "red": self.backgrounds = slice_and_assemble("assets/red_slice.png", (24, 24), (8, 8), (width, height))
        if color == "green": self.backgrounds = slice_and_assemble("assets/green_slice.png", (24, 24), (8, 8), (width, height))
        self.current_bg = 0

        self.justifyCenter  = justifyCenter
        self.alignCenter    = alignCenter
    
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def on_mouse_over(self):
        self.current_bg = 1
    def on_mouse_off(self):
        self.current_bg = 0
    def on_mouse_press(self):
        self.current_bg = len(self.backgrounds) - 1
    def on_mouse_release(self):
        self.current_bg = 0
        if self.callback is not None:
            self.callback()

    def render(self, surface: pygame.Surface):
        if self.justifyCenter: self.rect.x = (surface.get_width() - self.rect.width) / 2
        if self.alignCenter: self.rect.y = (surface.get_height() - self.rect.width) / 2
        
        surface.blit(self.backgrounds[self.current_bg], self.rect)

        pos = (
            self.rect.x + (self.rect.width - self.text.get_width()) / 2,
            self.rect.y + (self.rect.height - self.text.get_height()) / 2
        )

        surface.blit(self.text, pos)