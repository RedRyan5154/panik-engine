import pygame


class Image:
    def __init__(self, path, w=None, h=None):
        self.image = pygame.image.load(path).convert_alpha()
        if w and h:
            self.image = pygame.transform.scale(self.image, (w, h))
