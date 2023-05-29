from typing import List
import pygame

class Roll:
    def __init__(self, font: pygame.font.Font, pos_x: int, pos_y: int, callback = None):
        self.font = font
        self.pos_x, self.pos_y = pos_x, pos_y
        self.callback = callback

    def render(self, surface: pygame.Surface, list: List):
        pass

    def print_rooms(self, surface: pygame.Surface, rooms: List):
        (place, marker) = (0, 0)
        x = []
        room_names = []
        for room in rooms:
            room_names.append(room["room_name"])

        (room_names, x, place, marker) = self.file_master(surface, self.font, room_names, place, marker, x)


    def file_master(self, surface, font, room_names, place, marker, x):
        font_height = font.size(room_names[0])[1]
        screen_height = surface.get_height()
        max_file_width = 150
        name_max = 16 # how many maximum characters a list name can be 
        line = 65 # leave room at top of screen for other stuff
        col = 30 # where to start the first column
        count = 0
        for name in room_names[place:]:
            count += 1
            place += 1
            marker += 1
            if count >= 165 or place >= len(room_names):
                if len(name) > name_max:
                    name = name[:name_max] + '~'
                ren = font.render(name, True, (0, 0, 0))
                ren_rect = ren.get_rect()
                ren_rect[0] = col
                ren_rect[1] = line
                x.append((ren_rect, name))
                surface.blit(ren, ren_rect)
                print('space for next page, backspace for last page')
                return (room_names, x, 1, place, marker)
            if len(name) > name_max:
                name = name[:name_max] + '~'
            ren = font.render(name, True, (0, 0, 0))
            ren_rect = ren.get_rect()
            ren_rect[0] = col
            ren_rect[1] = line
            x.append((ren_rect, name))
            surface.blit(ren, ren_rect)
            line += 12
            if (line + font_height) >= (screen_height - 15):
                line = 65
                col += max_file_width

        return (room_names, x, 0, place, marker)
    
    # def handle_events(self):
    #     if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
    #         for item in x:
    #             if item[0].collidepoint(cursor):
    #                 print('you clicked ', item[1])
    #     if event.type == KEYDOWN and event.key == K_SPACE:
    #         print('space bar hit')
    #         if not place >= len(room_names):
    #             marker = 0
    #             x = []
    #             break
    #     if event.type == KEYDOWN and event.key == K_BACKSPACE:
    #         print('backspace hit')
    #         if ((place - marker) > 0):
    #             pygame.display.flip()
    #             place -= (165 + marker)
    #             marker = 0
    #             x = [] 
    #             break