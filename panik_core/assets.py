import pygame
import os

try:
    import numpy as np

    has_numpy = 1
except:
    has_numpy = 0


class Image:
    def __init__(self, path):
        if type(path) == str:
            self.image = pygame.image.load(path).convert_alpha()
        else:
            self.image = path

    def rotate(self, deg):
        self.image = pygame.transform.rotate(self.image, deg)


class ImageStack:
    def __init__(self, image_stack, layers) -> None:
        self.stack = pygame.image.load(image_stack).convert_alpha()
        self.w = self.stack.get_width()

        self.ln = layers

        try:
            self.h = self.stack.get_height() / layers
        except:
            raise Exception("Image stack doesn't have that amount of layers")

        self.layers = []
        for y in range(layers):
            self.layers.append(
                self.image_at(pygame.Rect(0, y * self.h, self.w, self.h))
            )

    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.stack, (0, 0), rect)

        if has_numpy:
            if not np.any(pygame.surfarray.array_alpha(image) == 0):
                image = pygame.Surface(rect.size, depth=32).convert()
                image.blit(self.stack, (0, 0), rect)
        return image


class Animation:
    def __init__(self, path):
        self.uanimations = {}
        self.animations = {}
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                out = os.path.join(path, filename)
                key = filename[:-4]
                self.uanimations[key] = pygame.image.load(out).convert_alpha()
                if has_numpy:
                    if not np.any(
                        pygame.surfarray.array_alpha(self.uanimations[key]) == 0
                    ):
                        self.uanimations[key] = pygame.image.load(out).convert()

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
        image.blit(self.sheet, (0, 0), rect)

        if has_numpy:
            if not np.any(pygame.surfarray.array_alpha(image) == 0):
                image = pygame.Surface(rect.size, depth=32).convert()
                image.blit(self.sheet, (0, 0), rect)
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
