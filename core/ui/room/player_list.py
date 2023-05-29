from typing import List
import pygame
from core.ui.components.container import Container
from core.ui.components.roll import Roll

from core.ui.components.text import Text

class PlayerList:
    def __init__(self, width: int, height: int, pos_x: int, pos_y: int, color: pygame.Color = (100, 255, 100)):
        self.container = Container(width, height, color, pos_x, pos_y)
        self.container.add_text("Players", 20, pos_x, pos_y - 20, alignCenter=False, justifyCenter=False)
        self.font = pygame.font.SysFont("Roboto", 15)
        self.color = color

        # button_width, button_height = 100, 40

        # self.container.add_button("room#1", self.on_click_room, pos_x + 10, pos_y + 10, button_width, button_height, color="blue")
        # self.container.add_button("room#2", self.on_click_room, pos_x + 10, pos_y + 60, button_width, button_height, color="blue")
        # self.container.add_button("room#3", self.on_click_room, pos_x + 10, pos_y + 110, button_width, button_height, color="blue")
        # self.container.add_button("room#4", self.on_click_room, pos_x + 10, pos_y + 160, button_width, button_height, color="blue")

    def render(self, surface: pygame.Surface, players):
        self.container.render(surface)
        self.print_players(players)

    def print_players(self, players: List):
        # [{'user': {'username': 'oguzhan', 'score': 10}, 'player_id': 2, 'direction': 'bottom', 'pos': '2:493,580'}]
        player_names  = []
        for player in players:
            player_names.append([player["user"]["username"], player["user"]["score"]])

        self.list_master(self.container.background, player_names)

    def list_master(self, surface: pygame.Surface, players):
        surface.fill(self.color)
        font_height     = self.font.size(players[0][0])[1]

        text_gap = 150
        name_max = 16
        pos_y    = 10
        pos_x    = 10
        place    = 0

        for (n, s) in players[place:]:
            place += 1
                
            if len(n) > name_max:
                n = n[:name_max] + '~'
            name           = self.font.render(n, True, (0, 0, 0))
            name_rect      = name.get_rect()
            name_rect[0], name_rect[1] = pos_x, pos_y

            score        = self.font.render(str(s), True, (0, 0, 0))
            score_rect   = score.get_rect()
            score_rect[0], score_rect[1] = (pos_x + text_gap), pos_y

            surface.blit(name, name_rect)
            surface.blit(score, score_rect)
            pos_y += font_height