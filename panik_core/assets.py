import pygame
import os


class Image:
    def __init__(self, path):
        self.image = pygame.image.load(path).convert_alpha()


class Animation:
    def __init__(self, path):
        self.uanimations = {}
        self.animations = {}
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                out = os.path.join(path, filename)
                key = filename[:-4]
                self.uanimations[key] = pygame.image.load(out).convert_alpha()

        sorted_keys = sorted(self.uanimations.keys())
        for i in sorted_keys:
            self.animations[i] = self.uanimations[i]


class Font:
    def __init__(self, font=None, size=20):
        self.font = pygame.font.Font(font, size)