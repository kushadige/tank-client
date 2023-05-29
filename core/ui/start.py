# Connection with server on start
import pygame
from core.client import Client
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from core.ui.components.container import Container
from core.ui.components.text import Text

from core.ui.colors import *

clock = pygame.time.Clock()

class Start:
    def __init__(self):
        self.container = Container()

        self.container.add_text("Start Container", 30, 0, 180, alignCenter=False)

        self.text1 = Text("Waiting.", 50, 0, 100, BLACK)
        self.text2 = Text("Closed.", 50, 0, 100, RED)
        self.text3 = Text("Successful.", 50, 0, 100, GREEN)

        self.app_state = "exit"
        self.running = True

    def render(self, surface: pygame.Surface, app, client: Client):
        while self.running:
            self.handle_events()
            self.container.render(surface)

            if client.status == "waiting": self.text1.render(surface)
            elif client.status == "closed": self.text2.render(surface)
            else: 
                self.text3.render(surface)
                self.app_state = "menu"

            pygame.display.flip()
            clock.tick(120)
        app.state = self.app_state
        
    def handle_events(self):
        clicks  = pygame.mouse.get_pressed()
        pos     = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                if self.app_state == "exit":
                    self.running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.running = False
            if e.type == pygame.MOUSEMOTION and not clicks[0]:
                self.container.on_mouse_move(pos)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.container.on_mouse_press(pos)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.container.on_mouse_release(pos)
            
        