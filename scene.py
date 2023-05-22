from scenes.game import Game
from scenes.intro import Intro
from scenes.login import Login
from scenes.menu import Menu
from scenes.register import Register

class Scene:
    def __init__(self, screen, client):
        self.screen = screen
        self.scene_state = "intro"
        self.intro = Intro(client)
        self.menu = Menu(client, screen)
        self.login = Login(client, screen)
        self.register = Register(client, screen)
        self.game = Game(client, screen)

    def scene_manager(self):
        if self.scene_state == "intro":
            self.intro.draw(self)
        if self.scene_state == "menu":
            self.menu.draw(self)
        if self.scene_state == "login":
            self.login.draw(self)
        if self.scene_state == "register":
            self.register.draw(self)
        if self.scene_state == "game":
            self.game.draw(self)