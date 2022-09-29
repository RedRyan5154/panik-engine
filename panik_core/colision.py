import pygame


class Colision:
    def __init__(
        self,
        id,
        colisionposx=0,
        colisionposy=0,
        colisionsizex=100,
        colisionsizey=100,
        parent=False,
    ):
        self.id = id
        self.x = colisionposx
        self.y = colisionposy
        self.colisionsizex = colisionsizex
        self.colisionsizey = colisionsizey
        self.parent = parent
        self.type = "colision"
        self.showcolision = True
        self.colision = pygame.Rect(
            colisionposx - colisionsizex / 2,
            colisionposy - colisionsizey / 2,
            colisionsizex,
            colisionsizey,
        )

    def moveX(self, x):
        self.x += x
        self.colision.x += x

    def moveY(self, y):
        self.y += y
        self.colision.y += y

    def isColiding(self, colision):
        return pygame.Rect.colliderect(self.colision, colision.colision)
