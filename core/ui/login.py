import pygame
from core.globals import SCREEN_HEIGHT
from core.ui.colors import BLACK, GREEN

from core.ui.components.container import Container
from core.ui.components.text import Text

clock = pygame.time.Clock()

class Login:
    def __init__(self):
        self.username = ""
        self.password = ""

        self.button_width = 200
        self.button_height = 50

        self.container = Container()

        self.pos = ( SCREEN_HEIGHT - 4*(self.button_height+10) ) / 2
        self.container.add_textbox(0, self.pos, self.button_width, self.button_height, justifyCenter=True, callback=self.on_typing)
        self.container.add_textbox(0, self.pos + 60, self.button_width, self.button_height, justifyCenter=True, callback=self.on_typing)
        self.container.add_button("Login", self.on_login, 0, self.pos + 120, self.button_width, self.button_height, justifyCenter=True, color="yellow")

        self.login_info = Text("", 24, 0, self.pos + 190, BLACK, alignCenter=False)
        self.time_info  = Text("", 30, 0, self.pos + 220, GREEN, alignCenter=False)

        self.current_time = 0
        self.process_end_time = 0
        
        self.running = True
        
    def on_typing(self, txt):
        if self.container.get_active_textbox() == 0: self.username = txt
        else: self.password = txt

    def render(self, surface: pygame.Surface, app, client):
        self.client = client
        app.state = "exit"
        while self.running:
            self.handle_events()

            if client.login_status:
                self.login_info.change_text(client.login_msg)
            
            self.current_time = pygame.time.get_ticks()
            if client.login_status == "success":
                # Redirect lobby after 3 second
                self.time_info.change_text(f"{3 - int((self.current_time - self.process_end_time)/1000)}")
                if self.current_time - self.process_end_time > 3000:
                    app.state = "lobby"
                    self.reset()
                    self.running = False
            else:
                app.state = "menu"
                self.process_end_time = pygame.time.get_ticks()

            self.container.render(surface)
            self.login_info.render(surface)
            self.time_info.render(surface)

            pygame.display.flip()
            clock.tick(120)
        self.reset()
        
    def handle_events(self):
        clicks  = pygame.mouse.get_pressed()
        keys    = pygame.key.get_pressed()
        pos     = pygame.mouse.get_pos()

        active_tb = self.container.get_active_textbox()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
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

    def on_login(self):
        if self.username and self.password:
            self.client.login(self.username, self.password)
            self.username = ""
            self.password = ""
            self.container.erase_all()

    def reset(self):
        self.username = ""
        self.password = ""
        self.container.erase_all()
        self.process_end_time = 0
        self.current_time = 0
        self.login_info.change_text("")
        self.time_info.change_text("")
        self.running = True
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)