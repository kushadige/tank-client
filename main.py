import pygame, sys
import traceback
from scene import Scene
from client import Client
from constants import *

# General Setup
pygame.init()
clock = pygame.time.Clock()
icon = pygame.image.load("./assets/icon.png")

# Game Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("TCP Tank - Multiplayer")
pygame.display.set_icon(icon)

client = Client()
scene = Scene(screen, client)

while True: # Game Loop
    try:
        scene.scene_manager()
        clock.tick(60)
    except Exception as e:
        traceback.print_exc()
        print(f"\nERROR: {e}")
        client.close_active_sock()
        pygame.quit()
        sys.exit()
            