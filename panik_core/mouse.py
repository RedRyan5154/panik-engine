import pygame


class Mouse:
    def getMousePos():
        return pygame.mouse.get_pos()

    def setPos(x, y):
        pygame.mouse.set_pos((x, y))

    @property
    def mousex():
        return pygame.mouse.get_pos()[0]

    @property
    def mousey():
        return pygame.mouse.get_pos()[1]

    def leftClick():
        return pygame.mouse.get_pressed()[0]

    def middleClick():
        return pygame.mouse.get_pressed()[1]

    def rightClick():
        return pygame.mouse.get_pressed()[3]

    def hide():
        pygame.mouse.set_visible(False)

    def show():
        pygame.mouse.set_visible(True)
