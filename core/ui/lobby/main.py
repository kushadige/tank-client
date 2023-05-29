import pygame
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT

from core.ui.components.container import Container
from core.ui.lobby.chat import Chat
from core.ui.lobby.user_list import UserList
from core.ui.lobby.room_list import RoomList

clock = pygame.time.Clock()

class Lobby:
    def __init__(self):
        self.container = Container()
        self.container.add_text("LOBBY", 30, 0, 0)
        self.container.add_button("Logout", self.on_logout, SCREEN_WIDTH - 110, 10, 100, 40, color="red")
        self.container.add_button("Create Room", self.on_create_room, SCREEN_WIDTH - 160, 60, 150, 40, color="green")

        # Chat
        chat_width, chat_height = 250, 200
        self.chat = Chat(chat_width, chat_height, SCREEN_WIDTH - chat_width - 10, SCREEN_HEIGHT - chat_height - 10)

        # Room List
        room_list_width, room_list_height = SCREEN_WIDTH - chat_width - 30, SCREEN_HEIGHT - 150
        self.room_list = RoomList(room_list_width, room_list_height, 10, 140, callback=self.on_click_room)

        # Player List
        user_list_width, user_list_height = chat_width, room_list_height - chat_height - 10
        self.user_list = UserList(user_list_width, user_list_height, SCREEN_WIDTH - chat_width - 10, 140)

        self.app_state = "exit"
        self.running = True

    def on_logout(self):
        self.app_state = "menu"
        self.running = False

    def on_create_room(self):
        self.app_state = "create_room"
        self.running = False
    
    def on_click_room(self, room_name):
        self.client.enter_room(room_name)

    def render(self, surface: pygame.Surface, app, client):
        self.client = client
        while self.running:
            self.handle_events()
            self.container.render(surface)

            self.chat.render(surface)
            self.room_list.render(surface, client.rooms)
            self.user_list.render(surface, client.users)

            if client.player_id != None:
                self.app_state = "room"
                break

            pygame.display.flip()
            clock.tick(120)
        app.state = self.app_state
        self.reset()

    def handle_events(self):
        keys    = pygame.key.get_pressed()
        events  = pygame.event.get()
        clicks  = pygame.mouse.get_pressed()
        pos     = pygame.mouse.get_pos()

        self.chat.handle_events(keys, events, clicks, pos)

        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.MOUSEMOTION and not clicks[0]:
                self.container.on_mouse_move(pos)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.container.on_mouse_press(pos)
                self.room_list.on_click_room(pos)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.container.on_mouse_release(pos)

    def reset(self):
        self.app_state = "exit"
        self.running = True