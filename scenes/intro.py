import pygame, sys
from threading import Thread

from utils.main import draw_text, font

welcome_msg_1 = "Welcome to Two Dot - Multiplayer"
welcome_msg_2 = "Trying to connect to server..."
success_msg = "Connection success..."
failure_msg_1 = "Could not connect to server..."
failure_msg_2 = "(Press ESC to exit)"

current_time = 0
process_end_time = 0

class Intro:
    def __init__(self, client):
        self.client = client
        self.connection_status = "waiting"
        Thread(target=client.start, args=([self,])).start()

    def draw(self, scene):
        global current_time, process_end_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.close_active_sock()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.client.close_active_sock()
                    pygame.quit()
                    sys.exit()
                scene.scene_state = "menu"
        
        current_time = pygame.time.get_ticks()

        # Drawing
        scene.screen.fill((255, 200, 100))
        draw_text(scene.screen, welcome_msg_1, font(24), (0, 0, 0), False, 100)
        draw_text(scene.screen, welcome_msg_2, font(20), (0, 0, 0), False, 125)
        if self.connection_status != "waiting":
            if self.connection_status == "success":
                draw_text(scene.screen, success_msg, font(20), (0, 255, 0), False, 160)
                draw_text(scene.screen, f"{3 - int((current_time - process_end_time)/1000)}", font(30), (0, 255, 0), False, 190)
                # login menu screen 3 seconds after success
                if current_time - process_end_time > 3000:
                    scene.scene_state = "menu"
            else:
                draw_text(scene.screen, failure_msg_1, font(20), (255, 0, 0), False, 160)
                draw_text(scene.screen, failure_msg_2, font(25), (255, 0, 0), False, 220)
        else:
            process_end_time = pygame.time.get_ticks()

        pygame.display.flip()