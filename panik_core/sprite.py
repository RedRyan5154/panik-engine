import pygame
import time


class Sprite:
    def __init__(
        self,
        id,
        image,
        x,
        y,
        image_scale=100,
        rotation=0,
        flip=[False, False],
        parent=False,
        colisionoffsetx=0,
        colisionoffsety=0,
        colisionsizex=100,
        colisionsizey=100,
    ):
        self.id = id
        self.animationidx = 0
        self.starttime = time.time()
        self.parent = parent
        self.image_scale = image_scale
        self.flip = flip
        self.x, self.y = x, y
        self.rotation = rotation
        self.type = "entity"
        self.showcolision = True
        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image
        self.size_x = self.image_scale * self.image.get_width() / 100
        self.size_y = self.image_scale * self.image.get_height() / 100
        self.colisionoffsetx = colisionoffsetx
        self.colisionoffsety = colisionoffsety
        self.colisionsizex = colisionsizex
        self.colisionsizey = colisionsizey
        self.colision = pygame.Rect(
            self.x + colisionoffsetx - colisionsizex / 2,
            self.y + colisionoffsety - colisionsizey / 2,
            colisionsizex,
            colisionsizey,
        )
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )

    def moveX(self, x):
        self.x += x
        self.colision.x += x

    def moveY(self, y):
        self.y += y
        self.colision.y += y

    def tryMoveX(self, x, colisions=[]):
        self.x += x
        self.colision.x += x
        if self.isColidingGroup(colisions):
            self.x -= x
            self.colision.x -= x

    def tryMoveY(self, y, colisions=[]):
        self.y += y
        self.colision.y += y
        if self.isColidingGroup(colisions):
            self.y -= y
            self.colision.y -= y

    def isColidingGroup(self, colisiongroup=[]):
        if self.colision.collidelist(colisiongroup):
            return True
        return False

    def isColiding(self, colision):
        return pygame.Rect.colliderect(self.colision, colision.colision)

    def updatePosition(self):
        self.colision.x, self.colision.y = (
            self.x - self.size_x / 2 + self.parent.x,
            self.y - self.size_y / 2 + self.parent.y,
        )

    def animate(self, animation, animname=None, delay=0.1):
        if animname:
            self.image = animation.animations[animname]
            self.size_x, self.size_y = (
                self.image_scale * self.image.get_width() / 100,
                self.image_scale * self.image.get_height() / 100,
            )
            self.image = pygame.transform.flip(
                pygame.transform.rotate(
                    pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                    self.rotation,
                ),
                self.flip[0],
                self.flip[1],
            )
        else:
            if time.time() - self.starttime > delay:
                self.starttime = time.time()
                if self.animationidx >= len(animation.animations) - 1:
                    self.animationidx = 0
                else:
                    self.animationidx += 1
                self.image = list(animation.animations.values())[self.animationidx]
                self.size_x, self.size_y = (
                    self.image_scale * self.image.get_width() / 100,
                    self.image_scale * self.image.get_height() / 100,
                )
                self.image = pygame.transform.flip(
                    pygame.transform.rotate(
                        pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                        self.rotation,
                    ),
                    self.flip[0],
                    self.flip[1],
                )

    def setImage(self):
        if type(self.image) == str:
            self.image = pygame.image.load(self.image).convert_alpha()
        self.size_x, self.size_y = (
            self.image_scale * self.image.get_width() / 100,
            self.image_scale * self.image.get_height() / 100,
        )
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )
