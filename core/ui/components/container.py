import pygame
from typing import List
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from core.ui.components.button import Button
from core.ui.components.textbox import TextBox
from core.ui.components.text import Text
from core.ui.colors import *

class Container:
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, color: pygame.Color = LIGHT_BLUE, pos_x: int = 0, pos_y: int = 0):
        self.background = pygame.Surface((width, height))
        self.background.fill(color)

        self.width, self.height = width, height
        self.pos_x, self.pos_y  = pos_x, pos_y
        self.color              = color

        self.buttons: List[Button]      = []
        self.texts: List[Text]          = []
        self.textboxes: List[TextBox]   = []

    def add_button(self, text: str, callback, pos_x: int, pos_y: int, button_width: int, button_height: int, justifyCenter: bool = False, alignCenter: bool = False, color: str = "gray"):
        self.buttons.append(Button(text, callback, pos_x, pos_y, button_width, button_height, justifyCenter, alignCenter, color))
    def add_textbox(self, pos_x: int, pos_y: int, tb_width: int, tb_height: int, justifyCenter: bool = False, alignCenter: bool = False, callback = None):
        self.textboxes.append(TextBox(pos_x, pos_y, tb_width, tb_height, justifyCenter, alignCenter, callback))
    def add_text(self, text: str, size: int, pos_x: int, pos_y: int, color: pygame.Color = BLACK, justifyCenter: bool = True, alignCenter: bool = True):
        self.texts.append(Text(text, size, pos_x, pos_y, color, justifyCenter, alignCenter))

    def on_typing(self, txt: str):
        for tb in self.textboxes:
            if tb.active:
                tb.on_typing(txt)

    def on_erasing(self):
        for tb in self.textboxes:
            if tb.active:
                tb.on_erasing()

    def on_erase_all(self):
        for tb in self.textboxes:
            if tb.active:
                tb.erase_all()
    
    def erase_all(self):
        for tb in self.textboxes:
            tb.erase_all()

    def on_mouse_move(self, pos):
        on_mouse = ""

        for button in self.buttons:
            if button.collidepoint(pos):
                button.on_mouse_over()
                on_mouse = "button"
                break
            else:
                button.on_mouse_off()
        
        for tb in self.textboxes:
            if tb.collidepoint(pos):
                tb.on_mouse_over()
                on_mouse = "textbox"
                break
            else:
                tb.on_mouse_off()
        
        if on_mouse == "button": pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif on_mouse == "textbox": pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else: pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def on_mouse_press(self, pos):
        for button in self.buttons:
            if button.collidepoint(pos):
                button.on_mouse_press()
        for tb in self.textboxes:
            if tb.collidepoint(pos):
                tb.on_mouse_press()

    def on_mouse_release(self, pos):
        for button in self.buttons:
            if button.collidepoint(pos):
                button.on_mouse_release()
            else:
                button.on_mouse_off()
        for tb in self.textboxes:
            if tb.collidepoint(pos):
                tb.on_mouse_release()
                tb.active = True
            else:
                tb.on_mouse_off()
                tb.active = False

    def get_button_at(self, pos):
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if button.collidepoint(pos):
                return i
    
    def get_active_textbox(self):
        for i in range(len(self.textboxes)):
            tb = self.textboxes[i]
            if tb.active:
                return i

    def render(self, surface: pygame.Surface):
        surface.blit(self.background, (self.pos_x, self.pos_y))

        for button in self.buttons:
            button.render(surface)
        
        for tb in self.textboxes:
            tb.render(surface)

        for text in self.texts:
            text.render(surface)