import pygame
from core.globals import SCREEN_HEIGHT
from core.ui.components.container import Container

clock = pygame.time.Clock()

class Menu:
    def __init__(self):
        self.button_width = 200
        self.button_height = 50

        self.container = Container()

        pos = ( SCREEN_HEIGHT - 4*(self.button_height+10) ) / 2
        self.container.add_button("Login", self.on_login, 0, pos, self.button_width, self.button_height, justifyCenter=True)
        self.container.add_button("Register", self.on_register, 0, pos + 60, self.button_width, self.button_height, justifyCenter=True)
        self.container.add_button("Exit", self.on_exit, 0, pos + 120, self.button_width, self.button_height, justifyCenter=True)

        self.selected = 0
        self.running = True

    def render(self, surface: pygame.Surface, app, client):
        if client.user["username"]:
            client.logout()

        while self.running:
            self.handle_events()
            self.container.render(surface)
            pygame.display.flip()
            clock.tick(120)
            
        if self.selected == "login": app.state = "login"
        elif self.selected == "register": app.state = "register"
        else: app.state = "exit"
        self.reset()
        
    def handle_events(self):
        clicks  = pygame.mouse.get_pressed()
        pos     = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.MOUSEMOTION and not clicks[0]:
                self.container.on_mouse_move(pos)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.container.on_mouse_press(pos)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.container.on_mouse_release(pos)

    def reset(self):
        self.selected = 0
        self.running = True
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def on_login(self):
        self.selected = "login"
        self.running = False
    def on_register(self):
        self.selected = "register"
        self.running = False
    def on_exit(self):
        self.selected = "exit"
        self.running = False