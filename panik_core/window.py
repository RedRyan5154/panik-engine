import pygame
from pygame.locals import *
import time


class Window:
    def __init__(self, title, width, height, icon=None):
        self.title = title
        self.width = width
        self.height = height
        self.devmode = False
        self.showfps = False
        self.icon = icon
        self.bg = (255, 255, 255)
        self.queue = []
        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        if self.icon:
            pygame.display.set_icon(pygame.image.load(icon).convert_alpha())
        else:
            pygame.display.set_icon(
                pygame.image.load("panik_core/asstes/logolowres.png").convert_alpha()
            )
        # fps
        self.clock = pygame.time.Clock()
        self.font_fps = pygame.font.Font(None, 20)
        self.starttime = 0.0
        self.endtime = 0.0
        self.delta_time = 0.0

    @property
    def winsize(self):
        return pygame.display.get_surface().get_size()

    def blit(self, object=[]):
        self.queue.extend(object)

    def tick(self, fps=30):
        self.delta_time = self.clock.tick(fps) / 1000.0
        return self.delta_time

    def update(self, uimanager=None, ui=None):
        self.starttime = time.time()
        self.WIN.fill(self.bg)
        # all elements
        for el in self.queue:
            if el.parent:
                if not el.parent.hide:
                    if el.type == "element":
                        self.WIN.blit(
                            el.image,
                            (
                                el.x - el.size_x / 2 + el.parent.x,
                                el.y - el.size_y / 2 + el.parent.y,
                            ),
                        )
                    if el.type == "entity":
                        self.WIN.blit(
                            el.image,
                            (
                                el.x - el.size_x / 2 + el.parent.x,
                                el.y - el.size_y / 2 + el.parent.y,
                            ),
                        )
                        el.colision.x = (
                            el.x
                            + el.colisionoffsetx
                            - el.colisionsizex / 2
                            + el.parent.x
                        )
                        el.colision.y = (
                            el.y
                            + el.colisionoffsety
                            - el.colisionsizey / 2
                            + el.parent.y
                        )
                        if el.showcolision and self.devmode:
                            text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                            pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                            self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                    if el.type == "colision":
                        el.colision.x = el.x - el.colisionsizex / 2 + el.parent.x
                        el.colision.y = el.y - el.colisionsizey / 2 + el.parent.y
                        el.colision.w = el.colisionsizex
                        el.colision.h = el.colisionsizey
                        if el.showcolision and self.devmode:
                            text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                            pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                            self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
            else:
                if el.type == "element":
                    self.WIN.blit(
                        el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                    )
                if el.type == "entity":
                    self.WIN.blit(
                        el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                    )
                    el.colision.x = el.x + el.colisionoffsetx - el.colisionsizex / 2
                    el.colision.y = el.y + el.colisionoffsety - el.colisionsizey / 2
                    if el.showcolision and self.devmode:
                        text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                if el.type == "colision":
                    el.colision.x = el.x - el.colisionsizex / 2
                    el.colision.y = el.y - el.colisionsizey / 2
                    el.colision.w = el.colisionsizex
                    el.colision.h = el.colisionsizey
                    if el.showcolision and self.devmode:
                        text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
        self.queue = []
        # ui
        if uimanager:
            try:
                uimanager.manager.set_visual_debug_mode(self.devmode)
                uimanager.manager.update(float(self.delta_time))
                uimanager.manager.draw_ui(self.WIN)
                if ui:
                    for el in ui:
                        el.draw(self.delta_time)
            except Exception:
                print("Error")
        if self.showfps:
            text = self.font_fps.render(
                "FPS: " + str(round(self.clock.get_fps())), True, (0, 0, 0)
            )
            self.WIN.blit(text, (10, 15))
        pygame.display.update()
        self.endtime = time.time()
        return str((self.endtime - self.starttime) / 1000)[:5] + "ms"

    def setResizable(self):
        self.WIN = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def setFullscreen(self):
        self.WIN = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF, 16)

    def setTitle(self, title):
        pygame.display.set_caption(title)

    def setIcon(self, icon):
        pygame.display.set_icon(pygame.image.load(icon).convert_alpha())
