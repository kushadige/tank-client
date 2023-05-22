import pygame, sys

from components.button import Button
from components.textbox import TextBox
from utils.main import centered_x_y

register_box_color = (255, 200, 100)
bg_active = (175, 175, 175)
bg_passive = (200, 200, 200)

class Register:
    def __init__(self, client, screen):
        self.client = client
        self.screen = screen
        self.input = ""

        self.surface = pygame.Surface((300, 400))
        self.rect = self.surface.get_rect()
        self.rect.topleft = centered_x_y(self.screen, self.rect)

        self.blue_button = pygame.image.load("./assets/buttons/blue_button04.png")
        self.register_button = Button(self.screen, self.blue_button, text="REGISTER")

        self.username = ""
        self.password = ""
        self.tb_username = TextBox(self.screen, self.register_button.rect.width, 50)
        self.tb_password = TextBox(self.screen, self.register_button.rect.width, 50)
        
    def draw(self, scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.close_active_sock()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.tb_username.active = True
                    self.tb_password.active = True
                    scene.scene_state = "menu"
                if self.tb_username.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.username = ""
                    elif self.tb_username.input.get_width() < self.tb_username.rect.width - 12 and event.key != pygame.K_ESCAPE and event.key != pygame.K_TAB:
                        self.username += event.unicode
                if self.tb_password.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.password = ""
                    elif self.tb_password.input.get_width() < self.tb_password.rect.width - 12 and event.key != pygame.K_ESCAPE and event.key != pygame.K_TAB:
                        self.password += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tb_username.rect.collidepoint(event.pos):
                    self.tb_username.active = True
                    self.tb_username.background = bg_active
                else:
                    self.tb_username.active = False
                    self.tb_username.background = bg_passive
                if self.tb_password.rect.collidepoint(event.pos):
                    self.tb_password.active = True
                    self.tb_password.background = bg_active
                else:
                    self.tb_password.active = False
                    self.tb_password.background = bg_passive

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
            if self.tb_username.active:
                self.username = ""
            if self.tb_password.active:
                self.password = ""

        ## Drawing
        self.screen.fill((100, 255, 200))

        pygame.draw.rect(self.screen, register_box_color, self.rect, 0, 10)

        self.tb_username.draw(self.username, y=100)
        self.tb_password.draw(self.password, y=175)
        self.register_button.draw(y=250)

        pygame.display.flip()
    