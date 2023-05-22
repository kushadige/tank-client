import pygame

def draw_text(screen, text, font, color, centered = True, pos_y = 0):
    surface = font.render(text, True, color)
    rect = surface.get_rect()

    if not centered:
        screen.blit(surface, (centered_x(screen, rect), pos_y))
    else:
        screen.blit(surface, (centered_x(screen, rect), centered_y(screen, rect)))

def draw_text_with_pos(screen, text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def centered_x(surface, rect):
    return ((surface.get_width() - rect.width) / 2)

def centered_y(surface, rect):
    return ((surface.get_height() - rect.height) / 2)

def centered_x_y(surface, rect):
    return (centered_x(surface, rect), centered_y(surface, rect))

def font(size):
    font = pygame.font.Font("./assets/font.ttf", size)
    return font