import pygame
import time
import math


class TileMap:
    def __init__(self, tile_list, assets, scale, x, y):

        ## meta
        self.type = "tilemap"
        self.x = x
        self.y = y
        self.scale = scale
        self.assets = assets

        ## tile map
        self.tiles = []

        ## store tile map
        f = open(tile_list, "r")
        data = f.read()
        f.close()
        data = data.split("\n")

        for y, row in enumerate(data):
            _tmprow = []
            for x, tile in enumerate(list(row)):
                if assets[tile][0] != None:  ## if tile is not empty
                    if assets[tile][1]:  ## if tile has colision
                        _thing = (
                            pygame.transform.scale(
                                assets[tile][0].image,
                                (
                                    scale * assets[tile][0].image.get_width() / 100,
                                    scale * assets[tile][0].image.get_height() / 100,
                                ),
                            ),
                            pygame.Rect(
                                self.x + x,
                                self.y + y,
                                scale * assets[tile][0].image.get_width() / 100,
                                scale * assets[tile][0].image.get_height() / 100,
                            ),
                            assets[tile][2],
                        )
                        _tmprow.append(_thing)
                    else:
                        _thing = (
                            pygame.transform.scale(
                                assets[tile][0].image,
                                (
                                    scale * assets[tile][0].image.get_width() / 100,
                                    scale * assets[tile][0].image.get_height() / 100,
                                ),
                            ),
                            None,
                            assets[tile][2],
                        )
                        _tmprow.append(_thing)
                else:
                    _tmprow.append((None,))
            self.tiles.append(_tmprow)


class Text:
    def __init__(self, text, x, y, font=None, size=20, color=(0, 0, 0)):
        if type(font) == str or font == None:
            self.font = pygame.font.Font(font, size)
        else:
            self.font = font.font
        self.x = x
        self.y = y
        self.color = color
        self.text = self.font.render(text, True, self.color)

        self.type = "text"

    def render_text(self, text):
        self.text = self.font.render(text, True, self.color)


class Element:
    def __init__(self, image, x, y, scale=100, rotation=0, flip=[False, False]):

        ## check if image is pre loaded or not

        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image

        self.x, self.y = x, y
        self.w = scale * self.image.get_width() / 100
        self.h = scale * self.image.get_height() / 100
        self.scale = scale
        self.rotation = rotation
        self.flip = flip
        self.colision = None

        self.type = "element"

        ## perform the correct transformations

        self.prevrot = self.rotation

        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.w, self.h)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )

        ## animation data

        self.animationidx = 0
        self.starttime = time.time()

    # Colision ------------------------------------------------------------------------#

    def add_colision(self, id, relative_x, relative_y, w, h):
        self.id = id
        self.cx = relative_x
        self.cy = relative_y
        self.cw = w
        self.ch = h
        self.colision = pygame.Rect(
            self.x + relative_x - w / 2, self.y + relative_y - h / 2, w, h
        )

    def is_coliding(self, colision):
        if type(colision) == list:
            return self.colision.collidelist(colision)
        else:
            return self.colision.colliderect(colision)

    # Movement ------------------------------------------------------------------------#

    def move_in_direction(self, direction, pixels):
        direction = math.radians(direction)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.x += mx
        self.y += my

    def move_x(self, x):
        self.x += x

    def move_y(self, y):
        self.y += y

    def try_move_x(self, x, colisions=[]):
        self.x += x
        self.colision.x += x
        if self.is_coliding(colisions):
            self.x -= x
            self.colision.x -= x
            return False
        return True

    def try_move_y(self, y, colisions=[]):
        self.y += y
        self.colision.y += y
        if self.is_coliding(colisions):
            self.y -= y
            self.colision.y -= y
            return False
        return True

    # Image Manipulation --------------------------------------------------------------#

    def animate(self, animation, delay=0.1):
        if time.time() - self.starttime > delay:
            self.starttime = time.time()
            if self.animationidx >= len(animation.animations) - 1:
                self.animationidx = 0
            else:
                self.animationidx += 1
            self.image = list(animation.animations.values())[self.animationidx]
            self.size_x, self.size_y = (
                self.scale * self.image.get_width() / 100,
                self.scale * self.image.get_height() / 100,
            )
            self.image = pygame.transform.flip(
                pygame.transform.rotate(
                    pygame.transform.scale(self.image, (self.w, self.h)),
                    self.rotation,
                ),
                self.flip[0],
                self.flip[1],
            )

    def set_image(self, image):
        ## check if image is pre loaded or not

        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image

        ## perform the correct transformations

        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.w, self.h)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )

    def scale_image(self, scale):
        self.scale = scale
        self.w = scale * self.image.get_width() / 100
        self.h = scale * self.image.get_height() / 100

        self.image = pygame.transform.scale(self.image, (self.w, self.h))

    def resize_image(self, w, h):
        self.w = w
        self.h = h

        self.image = pygame.transform.scale(self.image, (self.w, self.h))

    def flip_image(self, flip=[False, False]):
        fx, fy = False, False
        if flip[0]:
            if not self.flip[0]:
                fx = True
        else:
            if self.flip[0]:
                fx = True
        if flip[1]:
            if not self.flip[1]:
                fy = True
        else:
            if self.flip[1]:
                fy = True

        self.flip = flip

        self.image = pygame.transform.flip(self.image, fx, fy)
