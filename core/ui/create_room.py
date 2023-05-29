import pygame
from core.globals import SCREEN_HEIGHT
from core.ui.colors import BLACK, GREEN

from core.ui.components.container import Container
from core.ui.components.text import Text

clock = pygame.time.Clock()

class CreateRoom:
    def __init__(self):
        self.room_name = ""

        self.button_width = 200
        self.button_height = 50

        self.container = Container()

        self.pos = ( SCREEN_HEIGHT - 4*(self.button_height+10) ) / 2
        self.container.add_text("Room Name:", 24, 0, self.pos, alignCenter=False)
        self.container.add_textbox(0, self.pos + 40, self.button_width, self.button_height, justifyCenter=True, callback=self.on_typing)
        self.container.add_button("Create", self.on_create, 0, self.pos + 100, self.button_width, self.button_height, justifyCenter=True, color="green")
        
        self.app_state = "exit"
        self.running = True
        
    def on_typing(self, txt):
        self.room_name = txt

    def render(self, surface: pygame.Surface, app, client):
        self.client = client
        while self.running:
            self.handle_events()
            self.container.render(surface)
            pygame.display.flip()
            clock.tick(120)
        self.reset()
        app.state = self.app_state
        
    def handle_events(self):
        clicks  = pygame.mouse.get_pressed()
        keys    = pygame.key.get_pressed()
        pos     = pygame.mouse.get_pos()

        active_tb = self.container.get_active_textbox()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.app_state = "exit"
                self.running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.app_state = "lobby"
                    self.running = False
                elif e.key != pygame.K_RETURN and e.key != pygame.K_TAB and e.key != pygame.K_BACKSPACE:
                    if active_tb == 0 and len(self.room_name) < 15:
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

    def on_create(self):
        if self.room_name:
            self.client.create_room(self.room_name)
            self.room_name = ""
            self.container.erase_all()

    def reset(self):
        self.container.erase_all()
        self.room_name = ""
        self.running = True
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)