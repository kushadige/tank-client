import pygame, sys

clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.app_state = "exit"
        self.running = True
        
    def render(self, surface: pygame.Surface, app, client):
        self.client = client
        while self.running:
            self.handle_events()

            surface.fill((255, 255, 255))

            keys = pygame.key.get_pressed()
            if client.game_started:
                client.tank.rotate(keys)

                client.bullet_group.draw(surface)
                client.tank_group.draw(surface)

                client.bullet_group.update()
                client.tank_group.update(keys)
            
            pygame.display.flip()
            clock.tick(120)
        app.state = self.app_state
        self.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.client.leave_room()
                    self.app_state = "lobby"
                    self.running = False
                if event.key == pygame.K_SPACE:
                    #### SEND BULLET INFO TO OTHER CLIENTS WHEN SHOOT ####
                    reply = {
                        "command": "SHOT",
                        "data": {
                            "player_id": self.client.player_id
                        }
                    }
                    self.client.send(reply)
                    ##########################################################
                    self.client.tank.shoot()

    def reset(self):
        self.app_state = "exit"
        self.running = True