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

        self.blue_button_passive = pygame.image.load("./assets/buttons/blue_button04.png")
        self.blue_button_active = pygame.image.load("./assets/buttons/blue_button05.png")
        self.register_button = Button(self.screen, self.blue_button_passive, text="REGISTER")
        self.button_active = False

        self.username = ""
        self.password = ""
        self.confirm = ""
        self.tb_username = TextBox(self.screen, self.register_button.rect.width, 50)
        self.tb_password = TextBox(self.screen, self.register_button.rect.width, 50)
        self.tb_confirm = TextBox(self.screen, self.register_button.rect.width, 50)
        self.tb_active = False

    def register(self):
        # send register request to server
        pass
        
    def draw(self, scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.tb_username.active = False
                    self.tb_password.active = False
                    self.tb_confirm.active = False
                    self.username = ""
                    self.password = ""
                    self.confirm = ""
                    scene.scene_state = "menu"
                if self.tb_username.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_TAB:
                        self.tb_username.active = False
                        self.tb_password.active = True
                        self.tb_username.background = bg_passive
                        self.tb_password.background = bg_active
                    elif self.tb_username.input.get_width() < self.tb_username.rect.width - 20 and event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
                        self.username += event.unicode
                elif self.tb_password.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    elif event.key == pygame.K_TAB:
                        self.tb_password.active = False
                        self.tb_confirm.active = True
                        self.tb_password.background = bg_passive
                        self.tb_confirm.background = bg_active
                    elif self.tb_password.input.get_width() < self.tb_password.rect.width - 20 and event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
                        self.password += event.unicode
                elif self.tb_confirm.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.confirm = self.confirm[:-1]
                    elif event.key == pygame.K_TAB:
                        self.tb_confirm.active = False
                        self.tb_confirm.background = bg_passive
                    elif self.tb_confirm.input.get_width() < self.tb_confirm.rect.width - 20 and event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
                        self.confirm += event.unicode
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
                if self.tb_confirm.rect.collidepoint(event.pos):
                    self.tb_confirm.active = True
                    self.tb_confirm.background = bg_active
                else:
                    self.tb_confirm.active = False
                    self.tb_confirm.background = bg_passive
                if self.register_button.rect.collidepoint(event.pos):
                    self.client.register(self.username, self.password, self.confirm)
            if event.type == pygame.MOUSEMOTION:
                if self.register_button.rect.collidepoint(event.pos):
                    self.button_active = True
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self.register_button.update(self.blue_button_active)
                else:
                    self.button_active = False
                    self.register_button.update(self.blue_button_passive)
                    if not self.tb_active:
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if not self.button_active and (self.tb_username.rect.collidepoint(event.pos) or self.tb_password.rect.collidepoint(event.pos) or self.tb_confirm.rect.collidepoint(event.pos)):
                    self.tb_active = True
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                else:
                    self.tb_active = False
                    if not self.button_active:
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                if self.tb_username.rect.collidepoint(event.pos):
                    self.tb_username.background = bg_active
                else:
                    if not self.tb_username.active:
                        self.tb_username.background = bg_passive
                if self.tb_password.rect.collidepoint(event.pos):
                    self.tb_password.background = bg_active
                else:
                    if not self.tb_password.active:
                        self.tb_password.background = bg_passive
                if self.tb_confirm.rect.collidepoint(event.pos):
                    self.tb_confirm.background = bg_active
                else:
                    if not self.tb_confirm.active:
                        self.tb_confirm.background = bg_passive

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
            if self.tb_username.active:
                self.username = ""
            if self.tb_password.active:
                self.password = ""
            if self.tb_confirm.active:
                self.confirm = ""

        ## Drawing
        self.screen.fill((100, 255, 200))

        pygame.draw.rect(self.screen, register_box_color, self.rect, 0, 10)
        self.tb_username.draw(self.username, y=100)
        self.tb_password.draw("*" * len(self.password), y=175)
        self.tb_confirm.draw("*" * len(self.confirm), y=250)
        self.register_button.draw(y=325)

        pygame.display.flip()