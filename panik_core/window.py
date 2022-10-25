import pygame
from pygame.locals import *
import time
import random


class Window:
    class Camara:
        def __init__(self, x, y):
            self.x = x
            self.y = y

            self.chx = 0
            self.chy = 0

        def camara_shake(self, intensity):
            self.chx = random.randint(-intensity, intensity)
            self.chy = random.randint(-intensity, intensity)

    def __init__(self, title, width, height, icon=None):
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
        pygame.display.set_caption(title)
        if self.icon:
            pygame.display.set_icon(pygame.image.load(icon).convert_alpha())
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

    @property
    def winsize(self):
        return pygame.display.get_surface().get_size()

    def blit(self, object=[]):
        self.queue.extend(object)

    def tick(self, fps=30):
        self.delta_time = self.clock.tick(fps) / 1000.0
        return self.delta_time

    def setResizable(self):
        self.WIN = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def setFullscreen(self):
        self.WIN = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF, 16)

    def setTitle(self, title):
        pygame.display.set_caption(title)

    def setIcon(self, icon):
        pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

    def render(self, ui=None):
        self.starttime = time.time()  ## for timing

        self.WIN.fill(self.bg)  # clear the window

        ## main loop

        for element in self.queue:
            if element.type == "element":

                ## transform image

                if element.prevrot != element.rotation:
                    image = pygame.transform.rotate(element.image, element.rotation)
                else:
                    image = element.image

                element.prevrot = element.rotation

                ## center image
                draw_x = (
                    element.x - image.get_width() / 2 - self.camara.x - self.camara.chx
                )
                draw_y = (
                    element.y - image.get_height() / 2 - self.camara.y - self.camara.chy
                )

                ## blit image
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
                        self.WIN.blit(
                            text, (element.colision.x, element.colision.y - 25)
                        )
            elif element.type == "text":
                self.WIN.blit(
                    element.text,
                    (
                        element.x
                        - element.text.get_width() / 2
                        - self.camara.x
                        - self.camara.chx,
                        element.y
                        - element.text.get_height() / 2
                        - self.camara.y
                        - self.camara.chy,
                    ),
                )
            elif element.type == "tilemap":
                for y, row in enumerate(element.tiles):
                    for x, tile in enumerate(row):
                        if tile != None:
                            self.WIN.blit(
                                tile,
                                (
                                    element.x
                                    + x * tile.get_width()
                                    - self.camara.x
                                    - self.camara.chx,
                                    element.y
                                    + y * tile.get_height()
                                    - self.camara.y
                                    - self.camara.chy,
                                ),
                            )
                            if element.colisions[y][x]:
                                element.colisions[y][x].x = (
                                    element.x
                                    + x * tile.get_width()
                                    - self.camara.x
                                    - self.camara.chx
                                )

                                element.colisions[y][x].y = (
                                    element.y
                                    + y * tile.get_height()
                                    - self.camara.y
                                    - self.camara.chy
                                )
                        if self.devmode:
                            if element.colisions[y][x]:
                                pygame.draw.rect(
                                    self.WIN,
                                    (0, 0, 0),
                                    element.colisions[y][x],
                                    2,
                                )

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
            text = self.font.render(
                "FPS: "
                + str(round(self.clock.get_fps()))
                + " | MS: "
                + str(round(self.clock.get_time()))
                + " | DT: "
                + str(round(self.clock.get_rawtime())),
                True,
                self.fps_color,
            )
            self.WIN.blit(text, self.fps_pos)

        ## update and return timing

        self.queue = []

        pygame.display.update()
        self.endtime = time.time()
        return str((self.endtime - self.starttime) / 1000) + "ms"
