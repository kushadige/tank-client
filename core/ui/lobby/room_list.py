from typing import List
import pygame
from core.ui.components.container import Container
from core.ui.components.roll import Roll

from core.ui.components.text import Text

class RoomList:
    def __init__(self, width: int, height: int, pos_x: int, pos_y: int, color: pygame.Color = (100, 255, 100), callback = None):
        self.container = Container(width, height, color, pos_x, pos_y)
        self.container.add_text("Active Rooms", 20, pos_x + 10, pos_y - 20, alignCenter=False, justifyCenter=False)

        button_width, button_height = 100, 40

        self.container.add_button("room#1", self.on_click_room, pos_x + 10, pos_y + 10, button_width, button_height, color="blue")
        self.container.add_button("room#2", self.on_click_room, pos_x + 10, pos_y + 60, button_width, button_height, color="blue")
        self.container.add_button("room#3", self.on_click_room, pos_x + 10, pos_y + 110, button_width, button_height, color="blue")
        self.container.add_button("room#4", self.on_click_room, pos_x + 10, pos_y + 160, button_width, button_height, color="blue")

        self.callback           = callback

    def on_click_room(self, pos):
        room_name = ""
        if self.container.get_button_at(pos) == 0:
            room_name = "room#1"
        if self.container.get_button_at(pos) == 1:
            room_name = "room#2"
        if self.container.get_button_at(pos) == 2:
            room_name = "room#3"
        if self.container.get_button_at(pos) == 3:
            room_name = "room#4"
        if room_name:
            self.callback(room_name)

    def render(self, surface: pygame.Surface, rooms):
        self.container.render(surface)

    ####### TAMAMLANMADI
    def on_mouse_move(self, pos):
        for (room_name_rect, room_name) in self.ren_rooms:
            if room_name_rect.collidepoint(pos):
                room_name = self.font.render(room_name, True, (50, 200, 50))
                self.container.background.blit(room_name, room_name_rect)


    def print_rooms(self, surface: pygame.Surface, rooms: List):
        room_names  = []
        for room in rooms:
            room_names.append([room["room_name"], len(room["players"])])

        self.list_master(surface, room_names)

    def list_master(self, surface: pygame.Surface, room_names):
        font_height     = self.font.size(room_names[0][0])[1]
        parent_height   = self.container.background.get_height()

        text_gap = 150
        name_max = 16                  # how many maximum characters a list name can be 
        pos_y    = self.pos_y + 10     # leave room at top of screen for other stuff
        pos_x    = self.pos_x + 10     # where to start the first column
        place    = 0

        for (name, pcount) in room_names[place:]:
            place += 1
                
            if len(name) > name_max:
                name = name[:name_max] + '~'
            room_name           = self.font.render(name, True, (0, 0, 0))
            room_name_rect      = room_name.get_rect()
            room_name_rect[0], room_name_rect[1] = pos_x, pos_y

            self.ren_rooms.append([room_name_rect, name])

            player_count        = self.font.render(str(pcount), True, (0, 0, 0))
            player_count_rect   = player_count.get_rect()
            player_count_rect[0], player_count_rect[1] = (pos_x + text_gap), pos_y

            if not (pos_y + font_height) >= (parent_height + self.pos_y - 20):
                surface.blit(room_name, room_name_rect)
                surface.blit(player_count, player_count_rect)
                pos_y += font_height