import pygame
import os

import numpy as np


class Image:
    def __init__(self, path):
        self.image = pygame.image.load(path).convert_alpha()

        if not np.any(pygame.surfarray.array_alpha(self.image) == 0):
            self.image = pygame.image.load(path).convert()


class Animation:
    def __init__(self, path, spritesheet_length=None):
        if path.endswith(".png"):
            self.sheet = pygame.image.load(path).convert_alpha()
            self.animations = {}
            self.uanimations = {}
            for x in range(spritesheet_length - 1):
                self.uanimations[x] = self.image_at(
                    (
                        (self.sheet.get_width() / spritesheet_length) * x,
                        0,
                        self.sheet.get_width() / spritesheet_length,
                        self.sheet.get_height(),
                    )
                )
            sorted_keys = sorted(self.uanimations.keys())
            for i in sorted_keys:
                self.animations[i] = self.uanimations[i]
        else:
            self.uanimations = {}
            self.animations = {}
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    out = os.path.join(path, filename)
                    key = filename[:-4]
                    self.uanimations[key] = pygame.image.load(out).convert_alpha()
                    if not np.any(
                        pygame.surfarray.array_alpha(self.uanimations[key]) == 0
                    ):
                        self.uanimations[key] = pygame.image.load(out).convert()

            sorted_keys = sorted(self.uanimations.keys())
            for i in sorted_keys:
                self.animations[i] = self.uanimations[i]

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        array_alpha = pygame.surfarray.array_alpha(image)

        if np.all(array_alpha == 0):
            image = None
        elif not np.any(array_alpha == 0):
            image = pygame.Surface(rect.size, depth=32).convert()
            image.blit(self.sheet, (0, 0), rect)

        return image


class TileSet:
    def __init__(self, tileset):
        self.type = "tileset"
        self.sheet = pygame.image.load(tileset).convert_alpha()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        array_alpha = pygame.surfarray.array_alpha(image)

        if np.all(array_alpha == 0):
            image = None
        elif not np.any(array_alpha == 0):
            image = pygame.Surface(rect.size, depth=32).convert()
            image.blit(self.sheet, (0, 0), rect)

        return image

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
                images.append(img)

        res = {str(v): k for v, k in enumerate(images)}
        rres = {}
        for k, v in res.items():
            if v != None:
                rres[k] = v
        return rres

    def image_at_coll(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        array_alpha = pygame.surfarray.array_alpha(image)

        if np.all(array_alpha == 0):
            image = None
        elif not np.any(array_alpha == 0):
            image = pygame.Surface(rect.size, depth=32).convert()
            image.blit(self.sheet, (0, 0), rect)

        # resulting image and margins (left, right, up, down)
        res = [image, 0, 0, 0, 0]

        # get empty rows and columns
        if image:
            # col left
            idx = 0
            while np.all(array_alpha[idx, :] == 0):
                idx += 1
            if idx > 0:
                res[1] = idx
            # col right
            idx = -1
            while np.all(array_alpha[idx, :] == 0):
                idx -= 1
            if idx < -1:
                res[2] = abs(idx + 1)
            # row up
            idx = 0
            while np.all(array_alpha[:, idx] == 0):
                idx += 1
            if idx > 0:
                res[3] = idx
            # row down
            idx = -1
            while np.all(array_alpha[:, idx] == 0):
                idx -= 1
            if idx < -1:
                res[4] = abs(idx + 1)
        return res

    def load_coll(self, tile_dimensions=16):
        images = []
        for x in range(int(self.sheet.get_height() / tile_dimensions)):
            for y in range(int(self.sheet.get_width() / tile_dimensions)):
                img = self.image_at_coll(
                    (
                        y * tile_dimensions,
                        x * tile_dimensions,
                        tile_dimensions,
                        tile_dimensions,
                    )
                )
                images.append((img[0], (img[1:5])))

        res = {str(v): k for v, k in enumerate(images)}
        rres = {}
        for k, v in res.items():
            if v != None:
                rres[k] = v
        return rres


class ImageStack:
    def __init__(self, image_stack, layers) -> None:
        self.stack = pygame.image.load(image_stack).convert_alpha()
        self.num_layers = layers

    def load(self, scale):
        self.stack = pygame.transform.scale(
            self.stack,
            pygame.math.Vector2(self.stack.get_size()) * scale / 100,
        )
        self.w = self.stack.get_width()

        try:
            self.h = self.stack.get_height() / self.num_layers
        except:
            raise Exception("Image stack doesn't have that amount of layers")

        self.layers = []
        for y in range(self.num_layers):
            self.layers.append(
                self.image_at(pygame.Rect(0, y * self.h, self.w, self.h))
            )

    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.stack, (0, 0), rect)

        if not np.any(pygame.surfarray.array_alpha(image) == 0):
            image = pygame.Surface(rect.size, depth=32).convert()
            image.blit(self.stack, (0, 0), rect)
        return image


class Polygon:
    triangle = [
        pygame.math.Vector2(0, 0),
        pygame.math.Vector2(100, 200),
        pygame.math.Vector2(-100, 200),
    ]
