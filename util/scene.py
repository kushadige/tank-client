from typing import Union
import pygame

def font(size: int):
    font = pygame.font.Font(None, size)
    return font

############### MIDPONT #################
def midx(parent_rect: pygame.Rect, child: Union[pygame.Surface, pygame.Rect]):
    if isinstance(child, pygame.Surface):
        return (parent_rect.width - child.get_width()) / 2 
    elif isinstance(child, pygame.Rect):
        return (parent_rect.width - child.width) / 2 

def midy(parent_rect: pygame.Rect, child: Union[pygame.Surface, pygame.Rect]):
    if isinstance(child, pygame.Surface):
        return parent_rect.height - child.get_height() / 2
    elif isinstance(child, pygame.Rect):
        return (parent_rect.height - child.height) / 2 

def mid(parent_rect: pygame.Rect, child: Union[pygame.Surface, pygame.Rect]):
    return (midx(parent_rect, child), midy(parent_rect, child))


############### ADD TEXT ###################
def addtext(parent: pygame.Surface, parent_rect: pygame.Rect, text: str, font: pygame.font.Font, color: pygame.Color, pos_x: int = 0, pos_y: int = 0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if(pos_x == 0 and pos_y == 0):
        text_rect.topleft = mid(parent_rect, text_surface)
    elif(pos_x == 0 and pos_y != 0):
        text_rect.topleft = (midx(parent_rect, text_surface), pos_y)
    elif(pos_x != 0 and pos_y == 0):
        text_rect.topleft = (pos_x, midy(parent_rect, text_surface))
    else:
        text_rect.center = (pos_x, pos_y)

    parent.blit(text_surface, text_rect)