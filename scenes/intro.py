import pygame, sys
from threading import Thread

from utils.main import draw_text, font
from constants import *

current_time = 0
process_end_time = 0

class Intro:
    def __init__(self, client):
        self.client = client
        Thread(target=client.start).start()

    def draw(self, scene):
        global current_time, process_end_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.client.connection_status != "waiting":
                    self.client.stop()
                    pygame.quit()
                    sys.exit()
        
        current_time = pygame.time.get_ticks()

        # Drawing
        scene.screen.fill((255, 200, 100))
        draw_text(scene.screen, welcome_msg_1, font(24), (0, 0, 0), False, 100)
        draw_text(scene.screen, welcome_msg_2, font(20), (0, 0, 0), False, 125)
        if self.client.connection_status != "waiting":
            if self.client.connection_status == "success":
                draw_text(scene.screen, success_msg, font(20), (0, 255, 0), False, 160)
                draw_text(scene.screen, f"{3 - int((current_time - process_end_time)/1000)}", font(30), (0, 255, 0), False, 190)
                # login menu screen 3 seconds after success
                if current_time - process_end_time > 3000:
                    scene.scene_state = "menu"
                # scene.scene_state = "menu"
            else:
                draw_text(scene.screen, failure_msg_1, font(20), (255, 0, 0), False, 160)
                draw_text(scene.screen, failure_msg_2, font(25), (255, 0, 0), False, 220)
        else:
            process_end_time = pygame.time.get_ticks()

        pygame.display.flip()