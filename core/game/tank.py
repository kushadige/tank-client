import pygame
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from core.game.bullet import Bullet
from util.functions import rotate


class Tank(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, tid, client):
        super().__init__()
        self.surface = pygame.image.load(picture_path)
        self.image = self.surface
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

        self.direction  = "bottom"
        self.velocity   = 5
        self.health     = 100   # Hasar durumunda "DAMG" komutuyla diğer oyunculara bildirilir.
        self.tid        = tid
        
        self.client = client

    def update(self, keys):
        if self.client.player_id == self.tid:
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_UP]:
                reply = {
                    "command": "MOVE",
                    "data": {
                        "player_id": self.client.player_id,
                        "direction": self.direction,
                        "pos": str(self.client.player_id) + ":" + str(self.rect.centerx) + "," + str(self.rect.centery)
                    }
                }
                self.client.send(reply)
            if self.direction == "left" or self.direction == "right":
                self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.velocity
            if self.direction == "top" or self.direction == "bottom":
                self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.velocity
            if self.rect.bottom < 0:
                self.rect.y = SCREEN_HEIGHT
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            if self.rect.right < 0:
                self.rect.x = SCREEN_WIDTH
            if self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0

    def shoot(self):
        img = ""
        if self.tid == 0:
            img = "assets/bullets/bulletDark1_outline.png"
        elif self.tid == 1:
            img = "assets/bullets/bulletGreen1_outline.png"
        elif self.tid == 2:
            img = "assets/bullets/bulletSand1_outline.png"
        elif self.tid == 3:
            img = "assets/bullets/bulletBlue1_outline.png"
        
        new_bullet = Bullet(img, self.direction, self.rect.centerx, self.rect.centery)
        self.client.bullet_group.add(new_bullet)

    def rotate(self, keys):
        if keys[pygame.K_LEFT]:
            self.turn_left()
        elif keys[pygame.K_RIGHT]:
            self.turn_right()
        elif keys[pygame.K_UP]:
            self.turn_up()
        elif keys[pygame.K_DOWN]:
            self.turn_down()

    def turn_left(self):
        self.image, self.rect = rotate(self.surface, -90, self.rect.centerx, self.rect.centery)
        self.direction = "left"
    def turn_right(self):
        self.image, self.rect = rotate(self.surface, 90, self.rect.centerx, self.rect.centery)
        self.direction = "right"
    def turn_up(self):
        self.image, self.rect = rotate(self.surface, 180, self.rect.centerx, self.rect.centery)
        self.direction = "top"
    def turn_down(self):
        self.image, self.rect = rotate(self.surface, 0, self.rect.centerx, self.rect.centery)
        self.direction = "bottom"
    def change_img(self, img):
        self.surface = pygame.image.load(img)
        self.image = self.surface