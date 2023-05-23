import pygame, sys

from components.button import Button
from components.textbox import TextBox

from utils.main import centered_x_y

login_box_color = (255, 200, 100)
bg_active = (175, 175, 175)
bg_passive = (200, 200, 200)

class Login:
    def __init__(self, client, screen):
        self.client = client
        self.screen = screen
        self.input = ""

        self.surface = pygame.Surface((300, 400))
        self.rect = self.surface.get_rect()
        self.rect.topleft = centered_x_y(self.screen, self.rect)

        self.green_button_passive = pygame.image.load("./assets/buttons/green_button04.png")
        self.green_button_active = pygame.image.load("./assets/buttons/green_button05.png")
        self.login_button = Button(self.screen, self.green_button_passive, text="LOGIN")
        self.button_active = False

        self.username = ""
        self.password = ""
        self.tb_username = TextBox(self.screen, self.login_button.rect.width, 50)
        self.tb_password = TextBox(self.screen, self.login_button.rect.width, 50)
        self.tb_active = False
        
    def login(self):
        # send login request to server
        pass

    def draw(self, scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.close_active_sock()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.tb_username.active = False
                    self.tb_password.active = False
                    self.username = ""
                    self.password = ""
                    scene.scene_state = "menu"
                if self.tb_password.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    elif event.key == pygame.K_TAB:
                        self.tb_password.active = False
                        self.tb_password.background = bg_passive
                    elif self.tb_password.input.get_width() < self.tb_password.rect.width - 20 and event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
                        self.password += event.unicode
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
                if self.login_button.rect.collidepoint(event.pos):
                    print("login clicked!")
            if event.type == pygame.MOUSEMOTION:
                if self.login_button.rect.collidepoint(event.pos):
                    self.button_active = True
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self.login_button.update(self.green_button_active)
                else:
                    self.button_active = False
                    self.login_button.update(self.green_button_passive)
                    if not self.tb_active:
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if not self.button_active and (self.tb_username.rect.collidepoint(event.pos) or self.tb_password.rect.collidepoint(event.pos)):
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
            if self.tb_username.active:
                self.username = ""
            if self.tb_password.active:
                self.password = ""

        ## Drawing
        self.screen.fill((100, 255, 200))

        pygame.draw.rect(self.screen, login_box_color, self.rect, 0, 10)
        # draw_text(self.screen, "LOGIN", font(30), BLACK, False, 75)

        self.tb_username.draw(self.username, y=100)
        self.tb_password.draw("*" * len(self.password), y=175)
        self.login_button.draw(y=250)

        pygame.display.flip()
    