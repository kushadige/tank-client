import pygame
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from core.ui.components.button import Button

from core.ui.components.container import Container
from core.ui.room.player_list import PlayerList

clock = pygame.time.Clock()

class Room:
    def __init__(self):
        self.container = Container()
        self.container.add_text("ROOM", 30, 0, 0)
        self.container.add_button("Quit Room", self.on_leave_room, SCREEN_WIDTH - 160, 10, 150, 40, color="red")

        # Oda içi özel chat - TAMAMLANMADI
        # chat_width, chat_height = 250, 200
        # self.chat = Chat(chat_width, chat_height, SCREEN_WIDTH - chat_width - 10, SCREEN_HEIGHT - chat_height - 10)

        # Player List
        player_list_width, player_list_height = 150, 100
        self.player_list = PlayerList(player_list_width, player_list_height, 10, 140)

        # Start Game Button # odaya ilk bağlanan oyuncuya göster
        self.start_game_btn = Button("Start Game", self.on_start_game, 10, 140 + player_list_height + 20, 150, 40, color="green")

        self.app_state = "exit"
        self.running = True

    def on_start_game(self):
        self.client.start_game()
        self.app_state = "game"
        self.running = False

    def on_leave_room(self):
        self.client.leave_room()
        self.app_state = "lobby"
        self.running = False

    def render(self, surface: pygame.Surface, app, client):
        self.client = client
        while self.running:
            self.handle_events()
            self.container.render(surface)

            if len(client.active_room["players"]) > 0:
                self.player_list.render(surface, client.active_room["players"])

                if client.player_id == client.active_room["players"][0]["player_id"]:
                    self.start_game_btn.render(surface)

            if client.game_started:
                self.app_state = "game"
                break

            pygame.display.flip()
            clock.tick(120)
        app.state = self.app_state
        self.reset()

    def handle_events(self):
        events  = pygame.event.get()
        clicks  = pygame.mouse.get_pressed()
        pos     = pygame.mouse.get_pos()

        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.MOUSEMOTION and not clicks[0]:
                self.container.on_mouse_move(pos)
                if self.start_game_btn.collidepoint(pos):
                    self.start_game_btn.on_mouse_over()
                else:
                    self.start_game_btn.on_mouse_off()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.container.on_mouse_press(pos)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.container.on_mouse_release(pos)
                if self.start_game_btn.collidepoint(pos):
                    self.start_game_btn.on_mouse_release()
                else:
                    self.start_game_btn.on_mouse_off()

    def reset(self):
        self.app_state = "exit"
        self.running = True