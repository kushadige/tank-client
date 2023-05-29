import pygame, sys, traceback
from threading import Thread
from core.client import Client

from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT, DEST_IP, DEST_PORT
from core.ui.create_room import CreateRoom
from core.ui.game import Game
from core.ui.lobby.main import Lobby
from core.ui.login import Login
from core.ui.menu import Menu
from core.ui.room.main import Room
from core.ui.start import Start

class App:
    def __init__(self):
        # General Setup
        pygame.init()
        self.clock = pygame.time.Clock()
        self.clock.tick(120)

        # Client
        self.client = Client(DEST_IP, DEST_PORT)

        # Game Screen
        self.surface        = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.state          = "start"

        # Scenes
        self.start          = Start()
        self.menu           = Menu()
        self.login          = Login()
        # self.register     = Start()
        self.lobby          = Lobby()
        self.room           = Room()
        self.create_room    = CreateRoom()
        self.game           = Game()

        self.running = True
        
    def run(self):
        try:
            # Start client
            Thread(target=self.client.start, daemon=True).start()
            # Drawing
            self.game_loop()
        except Exception:
            traceback.print_exc()
            self.on_exit()

    def game_loop(self):
        while self.running:
            self.surface.fill((255, 255, 255))

            if self.state == "start":
                self.start.render(self.surface, self, self.client)
            elif self.state == "menu":
                self.menu.render(self.surface, self, self.client)
            elif self.state == "login":
                self.login.render(self.surface, self, self.client)
            # elif self.scene == "register":
            #     self.register.draw()
            elif self.state == "lobby":
                self.lobby.render(self.surface, self, self.client)
            elif self.state == "room":
                self.room.render(self.surface, self, self.client)
            elif self.state == "create_room":
                self.create_room.render(self.surface, self, self.client)
            elif self.state == "game":
                self.game.render(self.surface, self, self.client)
            else:
                break
        
        self.on_exit()
    
    def on_exit(self):
        if self.client.user["username"]:
            self.client.logout()
        if self.client.active_room["room_name"]:
            self.client.leave_room()
        self.client.stop()
        pygame.quit()
        sys.exit()

    def quit(self):
        self.running = False