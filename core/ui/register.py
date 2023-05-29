import pygame
from core.globals import SCREEN_HEIGHT

from core.ui.components.container import Container

clock = pygame.time.Clock()

class Login:
    def __init__(self):
        self.username       = ""
        self.password       = ""
        self.confirm        = ""

        self.button_width   = 200
        self.button_height  = 50

        self.container = Container()

        pos = ( SCREEN_HEIGHT - 3*(self.button_height+10) ) / 2
        self.container.add_textbox(0, pos, self.button_width, self.button_height, justifyCenter=True, callback=self.info)
        self.container.add_textbox(0, pos + 60, self.button_width, self.button_height, justifyCenter=True, callback=self.info)
        self.container.add_button("Login", self.on_login, 0, pos + 120, self.button_width, self.button_height, justifyCenter=True, color="yellow")

        self.running = True
        
    def info(self, txt):
        if self.container.get_active_textbox() == 0:
            self.username = txt
        else:
            self.password = txt
        print(self.username, self.password)

    def render(self, surface: pygame.Surface, app):
        while self.running:
            self.handle_events()
            self.container.render(surface)
            pygame.display.flip()
            clock.tick(120)
        app.state = "menu"
        self.reset()
        
    def handle_events(self):
        clicks  = pygame.mouse.get_pressed()
        keys    = pygame.key.get_pressed()
        pos     = pygame.mouse.get_pos()

        active_tb = self.container.get_active_textbox()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.running = False
                elif e.key != pygame.K_RETURN and e.key != pygame.K_TAB and e.key != pygame.K_BACKSPACE:
                    if active_tb == 0 and len(self.username) < 15 or active_tb == 1 and len(self.password) < 15:
                        self.container.on_typing(e.unicode)
                elif e.key == pygame.K_BACKSPACE:
                    self.container.on_erasing()
            if e.type == pygame.MOUSEMOTION and not clicks[0]:
                self.container.on_mouse_move(pos)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.container.on_mouse_press(pos)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.container.on_mouse_release(pos)
        
        if keys[pygame.K_BACKSPACE] and keys[pygame.K_LCTRL]:
            self.container.on_erase_all()

    def on_register(self):
        # self.app.state = "login"
        # self.running = False
        pass

    def reset(self):
        self.username   = ""
        self.password   = ""
        self.confirm    = ""
        self.running    = True
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)