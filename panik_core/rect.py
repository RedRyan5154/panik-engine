import pygame


class Rect:
    def __init__(
        self,
        id,
        x=0,
        y=0,
        sx=100,
        sy=100,
        color=(255, 255, 255),
        border=0,
        parent=False,
    ):
        self.id = id
        self.x = x
        self.y = y
        self.w = sx
        self.h = sy
        self.color = color
        self.border = border
        self.parent = parent
        self.type = "rect"
        self.colision = pygame.Rect(
            x - sx / 2,
            y - sy / 2,
            sx,
            sy,
        )

    def moveX(self, x):
        self.x += x
        self.colision.x += x

    def moveY(self, y):
        self.y += y
        self.colision.y += y

    def isColiding(self, colision):
        return pygame.Rect.colliderect(self.colision, colision.colision)
