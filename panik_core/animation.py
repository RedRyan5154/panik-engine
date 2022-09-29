import pygame
import os


class Animation:
    def __init__(self, animpath):
        self.animations = {}
        for filename in os.listdir(animpath):
            if filename.endswith(".png"):
                path = os.path.join(animpath, filename)
                key = filename[:-4]
                self.animations[key] = pygame.image.load(path).convert_alpha()
