import pygame, json

def rotate(surface, angle, pos_x, pos_y):
    surface_copy = pygame.transform.rotozoom(surface, angle, 1)
    # Re-calculate center point
    surface_copy_rect = surface_copy.get_rect(center = (pos_x, pos_y))
    return (surface_copy, surface_copy_rect)

def encode(data):
    plain_str = json.dumps(data, default=obj_dict)
    encoded_str = plain_str.encode()
    return encoded_str

def obj_dict(obj):
    return obj.__dict__