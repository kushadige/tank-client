import pygame
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from util.functions import rotate


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, direction, pos_x, pos_y):
        super().__init__()
        self.surface = pygame.image.load(picture_path)
        self.image = self.surface
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        
        self.direction  = direction
        self.velocity   = 7.5

        if(self.direction == "left"):
            self.image, self.rect = rotate(self.surface, 90, pos_x, pos_y)
        if(self.direction == "right"):
            self.image, self.rect = rotate(self.surface, -90, pos_x, pos_y)
        if(self.direction == "bottom"):
            self.image, self.rect = rotate(self.surface, 180, pos_x, pos_y)

    def update(self):
        if(self.direction == "left"):
            self.rect.x -= self.velocity
            if self.rect.x <= -100:
                self.kill()
        if(self.direction == "right"):
            self.rect.x += self.velocity
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
        if(self.direction == "top"):
            self.rect.y -= self.velocity
            if self.rect.y <= -100:
                self.kill()
        if(self.direction == "bottom"):
            self.rect.y += self.velocity
            if self.rect.top >= SCREEN_HEIGHT:
                self.kill()