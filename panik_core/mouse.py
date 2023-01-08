import pygame


def is_colliding(colision):
    if type(colision) == list:
        print("List")
        return not pygame.Rect(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1
        ).collidelist(colision)
    else:
        mouse = pygame.mouse.get_pos()
        return colision.collidepoint(mouse)

def mouse_pos():
    return pygame.mouse.get_pos()

def set_pos(x, y):
    pygame.mouse.set_pos((x, y))

def mouse_x():
    return pygame.mouse.get_pos()[0]

def mouse_y():
    return pygame.mouse.get_pos()[1]

def is_left_click():
    return pygame.mouse.get_pressed()[0]

def is_middle_click():
    return pygame.mouse.get_pressed()[1]

def is_right_click():
    return pygame.mouse.get_pressed()[2]

def hide():
    pygame.mouse.set_visible(False)

def show():
    pygame.mouse.set_visible(True)
