import pygame


class Parent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = "parent"
        self.hide = False

    def isPlayerColiding(self, player, colisiongroup=[]):
        for col in colisiongroup:
            if pygame.Rect.colliderect(player.colision, col.colision):
                return True
        return False
