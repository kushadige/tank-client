import pygame

from core.ui.components.textbox import TextBox

class Chat:
    def __init__(self, width: int, height: int, pos_x: int, pos_y: int, color: pygame.Color = (100, 100, 255)):
        self.background = pygame.Surface((width, height))
        self.background.fill(color)
        self.font = pygame.font.SysFont("Roboto", 13)

        self.width, self.height = width, height
        self.pos_x, self.pos_y  = pos_x, pos_y
        self.color              = color

        self.user_input = ""
        self.input_box = TextBox(self.pos_x, self.pos_y + self.height - 40, width, 40)

    def on_new_message(self):
        pass

    def handle_events(self, keys, events, clicks, pos):
        # keys = pygame.key.get_pressed()
        # if e.type == pygame.KEYDOWN:
        #     if e.key != pygame.K_RETURN and e.key != pygame.K_TAB and e.key != pygame.K_BACKSPACE and e.key != pygame.K_ESCAPE:
        #         if active_tb == 0 and len(self.username) < 15 or active_tb == 1 and len(self.password) < 15:
        #             container.on_typing(e.unicode)
        #     elif e.key == pygame.K_BACKSPACE:
        #         container.on_erasing()
        # if keys[pygame.K_BACKSPACE] and keys[pygame.K_LCTRL]:
        #     self.input_box.erase_all()
        # if e.type == pygame.MOUSEMOTION and not clicks[0]:
        #         self.container.on_mouse_move(pos)
        #     if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        #         self.container.on_mouse_press(pos)
        #     if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
        #         self.container.on_mouse_release(pos)
        pass

    def render(self, surface: pygame.Surface):
        surface.blit(self.background, (self.pos_x, self.pos_y))
        self.input_box.render(surface)

        # for button in self.buttons:
        #     button.render(surface)
        
        # for tb in self.textboxes:
        #     tb.render(surface)

        # for text in self.texts:
        #     text.render(surface)

# # Message Box
# message_box_width, message_box_height = 300, 200
# message_box_x, message_box_y = 100, 100
# message_box = pygame.Rect(message_box_x, message_box_y, message_box_width, message_box_height)
# message_box_color = (255, 255, 255)

# # Text Box
# input_box_height = 25
# input_box = pygame.Rect(message_box_x, message_box_y + message_box_height - input_box_height, message_box_width, input_box_height)
# input_box_active_color = (175, 175, 175)
# input_box_passive_color = (200, 200, 200)
# input_box_color = input_box_passive_color

# input_box_bg = pygame.Rect(message_box_x, message_box_y + message_box_height - input_box_height, message_box_width, input_box_height)
# input_box_bg_color = (225, 225, 225)

# input_box_active = False

# while True: # Game Loop
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if input_box.collidepoint(event.pos):
#                 input_box_active = True
#                 input_box_color = input_box_active_color
#             else:
#                 input_box_active = False
#                 input_box_color = input_box_passive_color
#         if event.type == pygame.KEYDOWN:
#             if input_box_active:
#                 if event.key == pygame.K_BACKSPACE:
#                     # delete last one
#                     user_input = user_input[0:-1] # or [0:-1]
#                 elif event.key == pygame.K_RETURN:
#                     # send message 
#                     user_input = ""
#                 elif text_input.get_width() < message_box_width - 12:
#                     user_input += event.unicode
            

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]:
#         user_input = ""
    
#     # Drawing
#     screen.fill(screen_bg_color)

#     pygame.draw.rect(screen, message_box_color, message_box, 0, 10)
#     pygame.draw.rect(screen, input_box_bg_color, input_box_bg)
#     pygame.draw.rect(screen, input_box_color, input_box, 2)

#     text_input = base_font.render(user_input, True, (0, 0, 0))
#     screen.blit(text_input, (input_box.x + 5, input_box.y + 5))
    
#     pygame.display.flip()
#     clock.tick(60)