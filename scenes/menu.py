import pygame, sys

from components.button import Button

class Menu:
    def __init__(self, client, screen):
        self.client = client
        self.screen = screen
        self.grey_button_passive = pygame.image.load("./assets/buttons/grey_button04.png")
        self.grey_button_active = pygame.image.load("./assets/buttons/grey_button05.png")
        self.login_button = Button(self.screen, self.grey_button_passive, text="Login")
        self.register_button = Button(self.screen, self.grey_button_passive, text="Register")
        self.exit_button = Button(self.screen, self.grey_button_passive, text="Exit")
        self.button_active = False
    def draw(self, scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.close_active_sock()
                pygame.quit()
                sys.exit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(self.login_button.rect.collidepoint(event.pos)):
                    scene.scene_state = "login"
                if(self.register_button.rect.collidepoint(event.pos)):
                    scene.scene_state = "register"
                if(self.exit_button.rect.collidepoint(event.pos)):
                    self.client.close_active_sock()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if self.login_button.rect.collidepoint(event.pos) or self.register_button.rect.collidepoint(event.pos) or self.exit_button.rect.collidepoint(event.pos):
                    self.button_active = True
                else:
                    self.button_active = False
                if self.login_button.rect.collidepoint(event.pos):
                    self.login_button.update(self.grey_button_active)
                else:
                    self.login_button.update(self.grey_button_passive)
                if self.register_button.rect.collidepoint(event.pos):
                    self.register_button.update(self.grey_button_active)
                else:
                    self.register_button.update(self.grey_button_passive)
                if self.exit_button.rect.collidepoint(event.pos):
                    self.exit_button.update(self.grey_button_active)
                else:
                    self.exit_button.update(self.grey_button_passive)
                if self.button_active:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

                
        self.screen.fill((100, 200, 255))
        self.login_button.draw(y=100)
        self.register_button.draw(y=175)
        self.exit_button.draw(y=250)

        pygame.display.flip()