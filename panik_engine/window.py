import pygame
from pygame.locals import *
import time
import random
import sys, math


class Window:
    class Queue:
        def __init__(self):
            self.queue = []

        def append(self, item):
            self.queue.append(item)

        def extend(self, item):
            self.queue.extend(item)

        def move(self, index, target_index):
            self.queue.insert(target_index, self.queue.pop(index))

        def __repr__(self):
            return f"[{len(self.queue)}]: {self.queue}"

    class Camara:
        def __init__(self, x, y):
            self.x = x
            self.y = y

            self.chx = 0
            self.chy = 0

            self.target = None

            self.lock_lag = 20

        def camara_shake(self, intensity):
            self.chx = random.randint(-intensity, intensity)
            self.chy = random.randint(-intensity, intensity)

        def camara_shake_float(self, intensity: int):
            """Give a int and camera shake will be 100 times smaller"""
            self.chx = random.randint(-intensity, intensity) / 100
            self.chy = random.randint(-intensity, intensity) / 100

        def lock_target(self, target):
            self.target = target

    def __init__(self, width, height, title=None, icon=None):
        """
        Creates a window

        > Title: The window title
        > Width/Height: The window dimensions

        (Optional)> Icon: The window icon. | Default: Panik-Core logo


        Editable Variables:

        > devmode: Shows collisions and other developer useful data to
        > bg: The Window background
        > showfps/showtiming: Display The FPS or frame delay
        > fpspos: Position of the FPS counter
        > fpscolor: Color of the FPS counter"""

        ## window data

        self.title = title
        self.width = width
        self.height = height
        self.devmode = False
        self.icon = icon
        self.bg = (255, 255, 255)
        self.WIN = pygame.display.set_mode((self.width, self.height))
        if title != None:
            pygame.display.set_caption(title)
        else:
            pygame.display.set_caption("Panik-Core Engine v.0.9.9")
        if self.icon:
            pygame.display.set_icon(
                pygame.transform.scale(
                    pygame.image.load(icon).convert_alpha(), (256, 256)
                )
            )
        else:
            pygame.display.set_icon(
                pygame.image.load("panik_engine/asstes/logolowres.png").convert_alpha()
            )

        ##fps

        self.showfps = False
        self.showtiming = False
        self.fps_pos = (10, 15)
        self.fps_color = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)
        self.starttime = 0.0
        self.endtime = 0.0
        self.delta_time = 0.0

        ## rendering data

        self.cam = self.Camara(0, 0)
        self.queue = self.Queue()

        ## cache
        self.winsize_cache = self.winsize

    @property
    def winsize(self):
        self.winsize_cache = pygame.display.get_surface().get_size()
        return pygame.display.get_surface().get_size()

    @property
    def gwidth(self):
        self.winsize_cache = pygame.display.get_surface().get_size()
        return pygame.display.get_surface().get_size()[0]

    @property
    def gheight(self):
        self.winsize_cache = pygame.display.get_surface().get_size()
        return pygame.display.get_surface().get_size()[1]

    def update(self, object=[]):
        """
        The list of game objects to be updated and ready for rendering.

        /!\ The order of the list is the order of rendering

        /!\ It's recommended to update all objects regarding if it should be renderd (use element.show = True|False)
        """
        self.queue.extend(object)

    def get_fps(self):
        return self.clock.get_fps()

    def tick(self, fps=30):
        self.delta_time = self.clock.tick(fps) / 1000.0
        return self.delta_time

    def setFullscreen(self):
        self.WIN = pygame.display.set_mode((0, 0), FULLSCREEN, 16)
        self.winsize_cache = self.winsize

    def setResizable(self):
        self.WIN = pygame.display.set_mode(self.winsize_cache, RESIZABLE, 16)
        self.winsize_cache = self.winsize

    def draw_rect(self, element, x, y, color):
        offset_vec = pygame.math.Vector2(x, y)
        res = []
        for vert in element.def_vertex:
            res.append(vert + offset_vec)
        for i, vertice in enumerate(res):
            pygame.draw.circle(
                self.WIN,
                color,
                vertice,
                4,
                4,
            )
        pygame.draw.lines(self.WIN, color, True, res, 4)
        pygame.draw.circle(
            self.WIN,
            color,
            (element.centroid + offset_vec),
            4,
            4,
        )

    def render(self, nofill=False, ui=None):
        self.starttime = time.time()  ## for timing

        if not nofill:
            self.WIN.fill(self.bg)  # clear the window

        ## do camara lock
        if self.cam.target:
            if self.cam.lock_lag:
                self.cam.x += (
                    (
                        (self.cam.target.x - self.cam.x - self.winsize[0] / 2)
                        * self.cam.lock_lag
                    )
                ) * self.delta_time
                self.cam.y += (
                    (
                        (self.cam.target.y - self.cam.y - self.winsize[1] / 2)
                        * self.cam.lock_lag
                    )
                ) * self.delta_time
            else:
                self.cam.x = self.cam.target.x - self.winsize_cache[0] / 2
                self.cam.y = self.cam.target.y - self.winsize_cache[1] / 2

        ## main loop
        for element in self.queue.queue:
            if element == None:
                continue
            elif element.type == "element":
                ## transform image

                ## rotate
                if element.rotation != 0:
                    if element.rotation > 360:
                        element.rotation = 0
                    elif element.rotation < 0:
                        element.rotation = 360
                    image = pygame.transform.rotate(element.texture, element.rotation)
                else:
                    image = element.texture

                ## center image
                draw_x = (
                    element.x
                    - image.get_width() / 2
                    - (self.cam.x if not element.is_hud else 0)
                    - (self.cam.chx if not element.is_hud else 0)
                )
                draw_y = (
                    element.y
                    - image.get_height() / 2
                    - (self.cam.y if not element.is_hud else 0)
                    - (self.cam.chy if not element.is_hud else 0)
                )

                ## blit image
                if element.show:
                    self.WIN.blit(image, (draw_x, draw_y))
                    if self.devmode:
                        pygame.draw.circle(
                            self.WIN,
                            (0, 255, 0),
                            (
                                draw_x + image.get_width() / 2,
                                draw_y + image.get_height() / 2,
                            ),
                            10,
                            5,
                        )
            elif element.type == "sprite":
                ## transform image

                ## rotate
                if element.rotation != 0:
                    if element.rotation > 360:
                        element.rotation = 0
                    elif element.rotation < 0:
                        element.rotation = 360
                    image = pygame.transform.rotate(element.texture, element.rotation)
                else:
                    image = element.texture

                ## center image
                draw_x = (
                    element.x
                    - element.center[0]
                    - image.get_width() / 2
                    - (self.cam.x if not element.is_hud else 0)
                    - (self.cam.chx if not element.is_hud else 0)
                    + (element.parent.x if element.parent else 0)
                )
                draw_y = (
                    element.y
                    - element.center[1]
                    - image.get_height() / 2
                    - (self.cam.y if not element.is_hud else 0)
                    - (self.cam.chy if not element.is_hud else 0)
                    + (element.parent.y if element.parent else 0)
                )

                ## blit image
                if element.show:
                    self.WIN.blit(image, (draw_x, draw_y))
                    if self.devmode:
                        pygame.draw.circle(
                            self.WIN,
                            (0, 255, 0),
                            (
                                draw_x + image.get_width() / 2 + element.center[0],
                                draw_y + image.get_height() / 2 + element.center[1],
                            ),
                            10,
                            5,
                        )
                ## collision
                if element.collision:
                    element.collision.update_vertexes()
                    element.collision.x = element.x + element.cx - element.cw / 2
                    element.collision.y = element.y + element.cy - element.ch / 2
                    if self.devmode and element.show:
                        self.draw_rect(
                            element.collision,
                            0
                            - (self.cam.x if not element.is_hud else 0)
                            - (self.cam.chx if not element.is_hud else 0)
                            + (element.parent.x if element.parent else 0),
                            0
                            - (self.cam.y if not element.is_hud else 0)
                            - (self.cam.chy if not element.is_hud else 0)
                            + (element.parent.y if element.parent else 0),
                            element.collision.color,
                        )
            elif element.type == "spritestack":
                if element.rotation > 360:
                    element.rotation = 0
                elif element.rotation < 0:
                    element.rotation = 360
                angle = element.rotation // element.va
                angle = int(angle % element.angles)

                image = element.cache[angle]

                draw_x = (
                    element.x
                    - image.get_width() / 2
                    - (self.cam.x if not element.is_hud else 0)
                    - (self.cam.chx if not element.is_hud else 0)
                )
                draw_y = (
                    element.y
                    - image.get_height() * 1.4 / 2
                    - (self.cam.y if not element.is_hud else 0)
                    - (self.cam.chy if not element.is_hud else 0)
                )

                if element.show:
                    self.WIN.blit(element.cache[angle], (draw_x, draw_y))

                if self.devmode:
                    pygame.draw.rect(
                        self.WIN,
                        (255, 0, 0),
                        (draw_x, draw_y, image.get_width(), image.get_height()),
                        4,
                    )
                    pygame.draw.circle(
                        self.WIN,
                        (0, 255, 0),
                        (
                            draw_x + image.get_width() / 2,
                            draw_y + image.get_height() * 1.4 / 2,
                        ),
                        10,
                        5,
                    )
            elif element.type == "collisionrect":
                element.update_vertexes()
                if element.show or self.devmode:
                    self.draw_rect(
                        element,
                        0
                        - (self.cam.x if not element.is_hud else 0)
                        - (self.cam.chx if not element.is_hud else 0),
                        0
                        - (self.cam.y if not element.is_hud else 0)
                        - (self.cam.chy if not element.is_hud else 0),
                        element.color,
                    )
            elif element.type == "tilemap":
                for y, row in enumerate(element.tiles):
                    if (  # if tile is off window, skip following collum rows
                        (y + 1) * element.tile_size
                        + element.y
                        - self.cam.y
                        - self.cam.chy
                        < 0
                    ):
                        continue
                    elif (
                        y * element.tile_size + element.y - self.cam.y - self.cam.chy
                        > self.winsize_cache[1]
                    ):
                        break
                    for x, tile in enumerate(row):
                        if tile != None:
                            if (  # if tile is off window, skip following collums
                                (x + 1) * element.tile_size
                                + element.x
                                - self.cam.x
                                - self.cam.chx
                                < 0
                            ):
                                continue
                            elif (
                                x * element.tile_size
                                + element.x
                                - self.cam.x
                                - self.cam.chx
                                > self.winsize_cache[0]
                            ):
                                break
                            self.WIN.blit(
                                element.tiles_lookup[tile],
                                (
                                    element.x
                                    + x * element.tile_size
                                    - self.cam.x
                                    - self.cam.chx,
                                    element.y
                                    + y * element.tile_size
                                    - self.cam.y
                                    - self.cam.chy,
                                ),
                            )
            elif element.type == "tilemapcol":
                if element.show:
                    for y, row in enumerate(element.tiles):
                        if (  # if tile is off window, skip following collum rows
                            (y + 1) * element.tile_size
                            + element.y
                            - self.cam.y
                            - self.cam.chy
                            < 0
                        ):
                            continue
                        elif (
                            y * element.tile_size
                            + element.y
                            - self.cam.y
                            - self.cam.chy
                            > self.winsize[1]
                        ):
                            break
                        for x, tile in enumerate(row):
                            if tile != None:
                                if (  # if tile is off window, skip following collums
                                    (x + 1) * element.tile_size
                                    + element.x
                                    - self.cam.x
                                    - self.cam.chx
                                    < 0
                                ):
                                    continue
                                elif (
                                    x * element.tile_size
                                    + element.x
                                    - self.cam.x
                                    - self.cam.chx
                                    > self.winsize[0]
                                ):
                                    break
                                self.WIN.blit(
                                    element.tiles_lookup[tile][0],
                                    (
                                        element.x
                                        + x * element.tile_size
                                        - self.cam.x
                                        - self.cam.chx,
                                        element.y
                                        + y * element.tile_size
                                        - self.cam.y
                                        - self.cam.chy,
                                    ),
                                )
                for collision in element.collisions.values():
                    collision.x = (
                        collision.tx * element.tile_size + element.x + collision.ox
                    )
                    collision.y = (
                        collision.ty * element.tile_size + element.y + collision.oy
                    )
                    collision.update_vertexes()

                    if self.devmode:
                        self.draw_rect(
                            collision,
                            0 - self.cam.x - self.cam.chx,
                            0 - self.cam.y - self.cam.chy,
                            collision.color,
                        )
            elif element.type == "text":
                if element.show:
                    self.WIN.blit(
                        element.text,
                        (
                            element.x
                            - (self.camara.x if not element.is_hud else 0)
                            - (self.camara.chx if not element.is_hud else 0),
                            element.y
                            - (self.camara.y if not element.is_hud else 0)
                            - (self.camara.chy if not element.is_hud else 0),
                        ),
                    )

        self.cam.chx = 0
        self.cam.chy = 0

        ## ui
        if ui:
            try:
                ui.manager.set_visual_debug_mode(self.devmode)
                ui.manager.update(float(self.delta_time))
                ui.manager.draw_ui(self.WIN)
            except Exception as e:
                print(e)

        ## show fps

        if self.showfps:
            text = self.font.render(
                "FPS: " + str(round(self.clock.get_fps())),
                True,
                self.fps_color,
            )
            self.WIN.blit(text, self.fps_pos)
        elif self.showtiming:
            self.WIN.blit(
                self.font.render(
                    "FPS: " + str(round(self.clock.get_fps())), True, self.fps_color
                ),
                (self.fps_pos[0], self.fps_pos[1]),
            )

            self.WIN.blit(
                self.font.render(
                    "MS: " + str(round(self.clock.get_time())), True, self.fps_color
                ),
                (self.fps_pos[0], self.fps_pos[1] + 15),
            )

            self.WIN.blit(
                self.font.render(
                    "DT: " + str(round(self.clock.get_rawtime())), True, self.fps_color
                ),
                (self.fps_pos[0], self.fps_pos[1] + 30),
            )

        ## update and return timing

        self.queue.queue = []

        pygame.display.flip()

        self.endtime = time.time()

        return str((self.endtime - self.starttime) / 1000) + "ms"
        # return float((self.endtime - self.starttime) / 1000)
