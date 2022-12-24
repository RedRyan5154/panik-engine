import pygame
import os
import numpy as np


class Image:
    def __init__(self, path):
        if type(path) == str:
            self.image = pygame.image.load(path).convert_alpha()
        else:
            self.image = path

    def scale_image(self, scale):
        self.scale = scale
        self.w = scale * self.image.get_width() / 100
        self.h = scale * self.image.get_height() / 100

        self.image = pygame.transform.scale(self.image, (self.w, self.h))


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


class TileSet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.set_colorkey(None, pygame.RLEACCEL)
        image.blit(self.sheet, (0, 0), rect)
        # if np.any(pygame.surfarray.pixels_alpha(image) != 0):
        #     re = Image(image)
        #     return re
        # return None
        return Image(image)

    def load(self, tile_dimensions=16):
        images = []
        for x in range(int(self.sheet.get_height() / tile_dimensions)):
            for y in range(int(self.sheet.get_width() / tile_dimensions)):
                img = self.image_at(
                    (
                        y * tile_dimensions,
                        x * tile_dimensions,
                        tile_dimensions,
                        tile_dimensions,
                    )
                )
                if img != None:
                    images.append(img)
        return {str(v): k for v, k in enumerate(images)}


class Audio:
    def __init__(self, audio_file):
        self.audio_file = pygame.mixer.Sound(audio_file)
