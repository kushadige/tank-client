import pygame, sys

from components.button import Button

class Menu:
    def __init__(self, client, screen):
        self.client = client
        self.screen = screen
        self.grey_button = pygame.image.load("./assets/buttons/grey_button00.png")
        self.login_button = Button(self.screen, self.grey_button, text="Login")
        self.register_button = Button(self.screen, self.grey_button, text="Register")
        self.exit_button = Button(self.screen, self.grey_button, text="Exit")

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
                
        self.screen.fill((100, 200, 255))
        self.login_button.draw(y=100)
        self.register_button.draw(y=175)
        self.exit_button.draw(y=250)

        pygame.display.flip()