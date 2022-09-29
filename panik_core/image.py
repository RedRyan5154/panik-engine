import pygame


class Image:
    def __init__(self, path):
        self.image = pygame.image.load(path).convert_alpha()
