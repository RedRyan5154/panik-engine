import pygame
import time
import math
import random


class TileMap:
    def __init__(self, tile_list, tile_size, assets, scale, x, y, parent=None) -> None:
        ## meta
        self.type = "tilemap"
        self.x = x
        self.y = y
        self.scale = scale
        self.assets = assets
        self.tile_size = tile_size * scale / 100
        if not str(self.tile_size).endswith(".0"):
            self.tile_size = round(self.tile_size) - 1

        ## tile map
        self.tiles = []
        self.parent = parent

        ## store tile map
        f = open(tile_list, "r")
        data = f.read()
        f.close()
        data = data.split("\n")

        if data[len(data) - 1] == "":
            del data[len(data) - 1]

        self.width = len(data[0]) * self.tile_size
        self.height = len(data) * self.tile_size

        self.hide = False

        class Tile(pygame.sprite.Sprite):
            def __init__(self, x, y, tile_img, tilesize) -> None:
                super().__init__()
                self.image = tile_img
                self.rect = pygame.Rect(
                    x * tilesize,
                    y * tilesize,
                    tilesize,
                    tilesize,
                )
                self.colision_mask = pygame.mask.from_surface(self.image)
                self.x, self.y = x * tilesize, y * tilesize

            def update(self, cx, cy, csx, csy, px, py):
                self.rect.x = self.x - cx - csx + px
                self.rect.y = self.y - cy - csy + py

        for y, row in enumerate(data):
            for x, tile in enumerate(row.split(",")):
                if tile == "-1":
                    continue
                try:
                    _tile = pygame.transform.scale(
                        assets[tile].image,
                        (
                            scale * assets[tile].image.get_width() / 100,
                            scale * assets[tile].image.get_height() / 100,
                        ),
                    )
                except KeyError:
                    raise Exception(
                        "The tilemap and tileset do not accord to the same tile. MAYBIE YOU HAVE LINKED THE WRONG TILESET OR TILEMAP"
                    )
                self.tiles.append(Tile(x, y, _tile, self.tile_size))

        self.group = pygame.sprite.Group()
        self.group.add(self.tiles)


class Text:
    def __init__(self, text, x, y, font=None, size=20, color=(0, 0, 0), parent=None):
        if type(font) == str or font == None:
            self.font = pygame.font.Font(font, size)
        else:
            self.font = font.font
        self.x = x
        self.y = y
        self.color = color
        self.text = self.font.render(text, True, self.color)
        self.x = x - self.text.get_width() / 2
        self.y = y - self.text.get_height() / 2

        self.type = "text"
        self.parent = parent

    def render_text(self, text):
        self.text = self.font.render(text, True, self.color)


class Rect(pygame.Rect):
    def __init__(self, x, y, w, h, color=(255, 255, 255), parent=None):
        super().__init__(x, y, w, h)
        self.color = color
        self.type = "rect"
        self.parent = parent
        self.fill = True

    def is_coliding(self, colision):
        if type(colision) == list:
            return 1 if self.collidelist(colision) != -1 else 0
        else:
            if colision.type == "rect":
                return self.colliderect(colision)
            else:
                return self.colliderect(colision.colision)

    def try_move_x(self, x, colisions=[]):
        self.x += x
        if self.is_coliding(colisions):
            self.x -= x
            return False
        return True

    def try_move_y(self, y, colisions=[]):
        self.y += y
        if self.is_coliding(colisions):
            self.y -= y
            return False
        return True


class Element:
    def __init__(
        self, image, x, y, scale=100, rotation=0, flip=[False, False], parent=None
    ):

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
        self.parent = parent
        self.hide = False
        self.is_hud = False

        ## perform the correct transformations

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
        self.prevanimation = None

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
        self.colision_mask = pygame.mask.Mask((self.colision.w, self.colision.h))
        self.colision_mask.fill()

    def is_coliding(self, colision):
        if self.colision:
            if type(colision) == list:
                return 1 if self.colision.collidelist(colision) != -1 else 0
            else:
                if colision.type == "rect":
                    return self.colision.colliderect(colision)
                else:
                    return self.colision.colliderect(colision.colision)
        else:
            raise Exception("You dont have any colisions set up for this element")

    def is_coliding_tilemap(self, tilemap):
        def check(sprite, tilemap):
            for group_sprite in tilemap:
                xoffset = group_sprite.rect.x - sprite.colision.x
                yoffset = group_sprite.rect.y - sprite.colision.y
                if sprite.colision_mask.overlap(
                    group_sprite.colision_mask, (xoffset, yoffset)
                ):
                    return 1
            return 0

        if self.colision_mask:
            return 1 if check(self, tilemap.group) else 0
        else:
            raise Exception("You dont have any colisions set up for this element")

    # Movement ------------------------------------------------------------------------#

    def move_in_direction(self, direction, pixels) -> tuple[float, float, float]:
        """
        Move in direction (direction) (pixels) pixels
        Return: x, y, direction
        """
        direction = math.radians(direction)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.move_x(mx)
        self.move_y(my)
        return mx, my, math.degrees(direction)

    def try_move_in_direction(
        self, direction, pixels, colisions=[]
    ) -> tuple[float, float, bool, bool, float]:
        """
        Try move in direction (direction) (pixels) pixels
        Return: x, y, has_collided_x, has_collided_y, direction
        """
        direction = math.radians(direction)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        cx = self.try_move_x(mx, colisions)
        cy = self.try_move_y(my, colisions)
        return mx, my, cx, cy, math.degrees(direction)

    def try_move_in_direction_tilemap(
        self, direction, pixels, tilemap
    ) -> tuple[float, float, bool, bool, float]:
        """
        Try move in direction (direction) (pixels) pixels
        Return: x, y, has_collided_x, has_collided_y, direction
        """
        direction = math.radians(direction)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        cx = self.try_move_x_tilemap(mx, tilemap)
        cy = self.try_move_y_tilemap(my, tilemap)
        return mx, my, cx, cy, math.degrees(direction)

    def move_towards(self, x, y, pixels) -> tuple[float, float, float]:
        """
        Move towards x/y
        TIP: If using the camera, add the camera x and y to the initial x and y
        Example: player.move_towards(x-self.window.camara.x, y-self.window.camara.y, 30)
        Return: x, y, direction
        """
        direction = -math.atan2(y - self.y, x - self.x)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.move_x(mx)
        self.move_y(my)
        return mx, my, math.degrees(direction)

    def try_move_towards(
        self, x, y, pixels, colisions=[]
    ) -> tuple[float, float, bool, bool, float]:
        """
        Try moving towards x/y
        TIP: If using the camera, add the camera x and y to the initial x and y
        Example: player.move_towards(x-self.window.camara.x, y-self.window.camara.y, 30)
        Return: x, y, has_collided_x, has_collided_y, direction
        """
        direction = -math.atan2(y - self.y, x - self.x)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        cx = self.try_move_x(mx, colisions)
        cy = self.try_move_y(my, colisions)
        return mx, my, cx, cy, math.degrees(direction)

    def try_move_towards_tilemap(
        self, x, y, pixels, tilemap
    ) -> tuple[float, float, bool, bool, float]:
        """
        Move towards x/y
        TIP: If using the camera, add the camera x and y to the initial x and y
        Example: player.move_towards(x-self.window.camara.x, y-self.window.camara.y, 30)
        Return: x, y, has_collided_x, has_collided_y, direction
        """
        direction = -math.atan2(y - self.y, x - self.x)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        cx = self.try_move_x_tilemap(mx, tilemap)
        cy = self.try_move_y_tilemap(my, tilemap)
        return mx, my, cx, cy, math.degrees(direction)

    def point_towards(self, x, y) -> float:
        """
        Point towards x/y
        TIP: If using the camera, add the camera x and y to the initial x and y
        Example: player.point_towards(x-self.window.camara.x, y-self.window.camara.y)
        """
        self.rotation = math.degrees(-math.atan2(y - self.y, x - self.x))
        return self.rotation

    def move_x(self, x):
        self.x += x

    def move_y(self, y):
        self.y += y

    def try_move_x(self, x, colisions=[]):
        if self.colision:
            self.x += x
            self.colision.x += x
            if self.is_coliding(colisions):
                self.x -= x
                self.colision.x -= x
                return False
            return True
        else:
            raise Exception("You dont have any colisions set up for this element")

    def try_move_y(self, y, colisions=[]):
        if self.colision:
            self.y += y
            self.colision.y += y
            if self.is_coliding(colisions):
                self.y -= y
                self.colision.y -= y
                return False
            return True
        else:
            raise Exception("You dont have any colisions set up for this element")

    def try_move_x_tilemap(self, x, tilemap):
        if self.colision:
            self.x += x
            self.colision.x += x
            if self.is_coliding_tilemap(tilemap):
                self.x -= x
                self.colision.x -= x
                return False
            return True
        else:
            raise Exception("You dont have any colisions set up for this element")

    def try_move_y_tilemap(self, y, tilemap):
        if self.colision:
            self.y += y
            self.colision.y += y
            if self.is_coliding_tilemap(tilemap):
                self.y -= y
                self.colision.y -= y
                return False
            return True
        else:
            raise Exception("You dont have any colisions set up for this element")

    # Image Manipulation --------------------------------------------------------------#

    def animate(self, animation, delay=0.1):
        if self.prevanimation != animation:
            self.animationidx = 0
            self.prevanimation = animation
            self.starttime = time.time() - delay
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
            self.image = pygame.transform.flip(self.image, self.flip[0], self.flip[1])
            self.scale_image(self.scale)

    def set_image(self, image):
        ## check if image is pre loaded or not

        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image

        ## perform the correct transformations
        self.image = pygame.transform.flip(self.image, self.flip[0], self.flip[1])
        self.scale_image(self.scale)

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


class Parent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Music:
    def __init__(self, audio_file):
        pygame.mixer.music.load(audio_file)

    def play(self, loops=0, fade_ms=0):
        pygame.mixer.music.play(loops, fade_ms=fade_ms)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def fade(self, fade):
        pygame.mixer.music.fadeout(fade)

    def queue(self, audio_file, loops=0):
        pygame.mixer.music.queue(audio_file, loops=loops)

    def set_volume(self, volume=100):
        pygame.mixer.music.set_volume(volume / 100)

    @property
    def volume(self):
        return pygame.mixer.music.get_volume()


class Sound:
    def __init__(self, audio_file, channel=0):
        self.audio = audio_file.audio_file
        self.channel = channel

    def play(self, loops=0, maxtime=0, fade_ms=0):
        pygame.mixer.Channel(int(self.channel)).play(
            self.audio, loops, maxtime, fade_ms
        )

    def stop(self):
        pygame.mixer.Channel(int(self.channel)).stop()

    def set_volume(self, volume=100):
        pygame.mixer.Channel(int(self.channel)).set_volume(volume / 100)
