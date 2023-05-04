import pygame
from pygame.locals import *
import time
import random
import sys, math


class Window:
    class Camara:
        def __init__(self, x, y):
            self.x = x
            self.y = y

            self.chx = 0
            self.chy = 0

            self.target = None

            self.lock_strength = 20

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

        > devmode: Shows colisions and other developer useful data to
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
            pygame.display.set_caption("Panik-Core Engine v.0.8.8")
        if self.icon:
            pygame.display.set_icon(
                pygame.transform.scale(
                    pygame.image.load(icon).convert_alpha(), (256, 256)
                )
            )
        else:
            pygame.display.set_icon(
                pygame.image.load("panik_core/asstes/logolowres.png").convert_alpha()
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

        self.camara = self.Camara(0, 0)
        self.queue = []

        ## cache
        self.winsize_cache = self.winsize

    @property
    def winsize(self):
        self.winsize_cache = pygame.display.get_surface().get_size()
        return pygame.display.get_surface().get_size()

    @property
    def wwidth(self):
        self.winsize_cache = pygame.display.get_surface().get_size()
        return pygame.display.get_surface().get_size()[0]

    @property
    def wheight(self):
        self.winsize_cache = pygame.display.get_surface().get_size()
        return pygame.display.get_surface().get_size()[1]

    def blit(self, object=[]):
        self.queue.extend(object)

    def tick(self, fps=30):
        self.delta_time = self.clock.tick(fps) / 1000.0
        return self.delta_time

    def setFullscreen(self):
        self.WIN = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF | HWACCEL, 16)
        self.winsize_cache = self.winsize

    def setResizable(self):
        self.WIN = pygame.display.set_mode(self.winsize_cache, RESIZABLE, 16)
        self.winsize_cache = self.winsize

    def render(self, nofill=False, ui=None):
        self.starttime = time.time()  ## for timing

        if not nofill:
            self.WIN.fill(self.bg)  # clear the window

        ## do camara lock
        if self.camara.target:
            self.camara.x += (self.camara.target.x-self.camara.x-self.winsize_cache[0]/2) / self.camara.lock_strength
            self.camara.y += (self.camara.target.y-self.camara.y-self.winsize_cache[1]/2) / self.camara.lock_strength

        ## main loop
        for element in self.queue:
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
                    image = pygame.transform.rotate(element.image, element.rotation)
                else:
                    image = element.image

                ## center image
                draw_x = (
                    element.x
                    - image.get_width() / 2
                    - (self.camara.x if not element.is_hud else 0)
                    - (self.camara.chx if not element.is_hud else 0)
                    + (element.parent.x if element.parent else 0)
                )
                draw_y = (
                    element.y
                    - image.get_height() / 2
                    - (self.camara.y if not element.is_hud else 0)
                    - (self.camara.chy if not element.is_hud else 0)
                    + (element.parent.y if element.parent else 0)
                )

                ## blit image
                if not element.hide:
                    self.WIN.blit(image, (draw_x, draw_y))

                ## colision
                if element.colision:
                    ## center colision
                    element.colision.x = (
                        element.x
                        + element.cx
                        - element.cw / 2
                        - self.camara.x
                        - self.camara.chx
                    )
                    element.colision.y = (
                        element.y
                        + element.cy
                        - element.ch / 2
                        - self.camara.y
                        - self.camara.chy
                    )

                    if self.devmode:
                        text = self.font.render("ID: " + element.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), element.colision, 4)
                        self.WIN.blit(text, (element.colision.x, element.colision.y - 25))
            elif element.type == "elementstack":
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
                    - (self.camara.x if not element.is_hud else 0)
                    - (self.camara.chx if not element.is_hud else 0)
                    + (element.parent.x if element.parent else 0)
                )
                draw_y = (
                    element.y
                    - image.get_height() * 1.4 / 2
                    - (self.camara.y if not element.is_hud else 0)
                    - (self.camara.chy if not element.is_hud else 0)
                    + (element.parent.y if element.parent else 0)
                )

                self.WIN.blit(element.cache[angle], (draw_x, draw_y))

                ## colision
                if element.colision:
                    ## center colision
                    element.colision.x = (
                        element.x
                        + element.cx
                        - element.cw / 2
                        - self.camara.x
                        - self.camara.chx
                    )
                    element.colision.y = (
                        element.y
                        + element.cy
                        - element.ch / 2
                        - self.camara.y
                        - self.camara.chy
                    )

                    if self.devmode:
                        text = self.font.render("ID: " + element.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), element.colision, 4)
                        self.WIN.blit(text, (element.colision.x, element.colision.y - 25))

                if self.devmode:
                    pygame.draw.rect(
                        self.WIN,
                        (255, 0, 0),
                        (draw_x, draw_y, image.get_width(), image.get_height()),
                        4,
                    )
                    pygame.draw.circle(
                        self.WIN,
                        (255, 0, 0),
                        (
                            draw_x + image.get_width() / 2,
                            draw_y + image.get_height() * 1.4 / 2,
                        ),
                        10,
                        5,
                    )
            elif element.type == "text":
                self.WIN.blit(
                    element.text,
                    (
                        element.x
                        - (self.camara.x if not element.is_hud else 0)
                        - (self.camara.chx if not element.is_hud else 0)
                        + (element.parent.x if element.parent else 0),
                        element.y
                        - (self.camara.y if not element.is_hud else 0)
                        - (self.camara.chy if not element.is_hud else 0)
                        + (element.parent.y if element.parent else 0),
                    ),
                )
            elif element.type == "tilemap":
                for y, row in enumerate(element.tiles):
                    if (  # if tile is off window, skip following collum rows
                        (y + 1) * element.tile_size
                        + element.y
                        - self.camara.y
                        - self.camara.chy
                        + (element.parent.y if element.parent else 0)
                        < 0
                    ):
                        continue
                    elif (
                        y * element.tile_size
                        + element.y
                        - self.camara.y
                        - self.camara.chy
                        + (element.parent.y if element.parent else 0)
                        > self.winsize_cache[1]
                    ):
                        break
                    for x, tile in enumerate(row):
                        if tile != None:
                            if (  # if tile is off window, skip following collums
                                (x + 1) * element.tile_size
                                + element.x
                                - self.camara.x
                                - self.camara.chx
                                + (element.parent.x if element.parent else 0)
                                < 0
                            ):
                                continue
                            elif (
                                x * element.tile_size
                                + element.x
                                - self.camara.x
                                - self.camara.chx
                                + (element.parent.x if element.parent else 0)
                                > self.winsize_cache[0]
                            ):
                                break
                            self.WIN.blit(
                                tile,
                                (
                                    element.x
                                    + x * element.tile_size
                                    - self.camara.x
                                    - self.camara.chx
                                    + (element.parent.x if element.parent else 0),
                                    element.y
                                    + y * element.tile_size
                                    - self.camara.y
                                    - self.camara.chy
                                    + (element.parent.y if element.parent else 0),
                                ),
                            )
            elif element.type == "rect":
                pygame.draw.rect(self.WIN, element.color, element)

        self.camara.chx = 0
        self.camara.chy = 0

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

        self.queue = []

        pygame.display.flip()

        self.endtime = time.time()

        return str((self.endtime - self.starttime) / 1000) + "ms"
        # return float((self.endtime - self.starttime) / 1000)
