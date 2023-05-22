import pygame, sys

from constants import BLACK
from utils.main import draw_text, font

class Game:
    def __init__(self, client, screen):
        self.client = client
        self.screen = screen
        
    def draw(self, scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                scene.scene_state = "menu"

        self.screen.fill((100, 255, 200))
        draw_text(self.screen, "GAME SCREEN", font(30), BLACK)
        
        pygame.display.flip()