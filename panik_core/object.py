import pygame
import time


class Object:
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
    ):
        self.id = id
        self.animationidx = 0
        self.starttime = time.time()
        self.parent = parent
        self.image_scale = image_scale
        self.flip = flip
        self.x, self.y = x, y
        self.rotation = rotation
        self.type = "element"
        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image
        self.size_x = self.image_scale * self.image.get_width() / 100
        self.size_y = self.image_scale * self.image.get_height() / 100
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
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
