import pygame
from pygame.locals import *
import time


class Subwindow:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect((width, height), (x, y))
        self.parent = None
        self.id = "Sub"
        self.devmode = False
        self.type = "sub"
        self.bg = (255, 255, 255)
        self.queue = []
        self.WIN = pygame.Surface((width, height))
        pygame.transform.scale(self.WIN, (self.width, self.height))

        self.font_fps = pygame.font.Font(None, 20)
        self.starttime = 0.0
        self.endtime = 0.0

    def updateSize(self):
        self.WIN = pygame.transform.scale(self.WIN, (self.width, self.height))

    @property
    def winsize(self):
        return pygame.display.get_surface().get_size()

    @property
    def mousePos(self):
        pos = pygame.mouse.get_pos()
        return (
            pos[0] - self.rect.x,
            pos[1] - self.rect.y,
        )

    def blit(self, object=[]):
        self.queue.extend(object)

    def update(self, uimanager=None, ui=None, post=[]):
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
                    elif el.type == "entity":
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
                        if el.showcolision or self.devmode:
                            text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                            pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                            self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                    elif el.type == "colision":
                        el.colision.x = el.x - el.colisionsizex / 2 + el.parent.x
                        el.colision.y = el.y - el.colisionsizey / 2 + el.parent.y
                        el.colision.w = el.colisionsizex
                        el.colision.h = el.colisionsizey
                        if el.showcolision or self.devmode:
                            text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                            pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                            self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                    elif el.type == "rect":
                        el.colision.x = el.x - el.w / 2 + el.parent.x
                        el.colision.y = el.y - el.h / 2 + el.parent.y
                        el.colision.w = el.w
                        el.colision.h = el.h
                        pygame.draw.rect(self.WIN, el.color, el.colision, el.border)
                    elif el.type == "text":
                        print(el.x)
                        self.WIN.blit(el.text, (el.x, el.y))
            else:
                if el.type == "sub":
                    self.WIN.blit(
                        el.WIN,
                        (
                            el.x - el.width / 2,
                            el.y - el.height / 2,
                        ),
                    )
                elif el.type == "element":
                    self.WIN.blit(
                        el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                    )
                elif el.type == "entity":
                    self.WIN.blit(
                        el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                    )
                    el.colision.x = el.x + el.colisionoffsetx - el.colisionsizex / 2
                    el.colision.y = el.y + el.colisionoffsety - el.colisionsizey / 2
                    if el.showcolision or self.devmode:
                        text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                elif el.type == "colision":
                    el.colision.x = el.x - el.colisionsizex / 2
                    el.colision.y = el.y - el.colisionsizey / 2
                    el.colision.w = el.colisionsizex
                    el.colision.h = el.colisionsizey
                    if el.showcolision or self.devmode:
                        text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                elif el.type == "rect":
                    el.colision.x = el.x - el.w / 2
                    el.colision.y = el.y - el.h / 2
                    el.colision.w = el.w
                    el.colision.h = el.h
                    pygame.draw.rect(self.WIN, el.color, el.colision, el.border)
                elif el.type == "text":
                    self.WIN.blit(el.text, (el.x, el.y))
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
                for el in post:
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
                                if el.showcolision or self.devmode:
                                    text = self.font_fps.render(
                                        "ID: " + el.id, True, (0, 0, 0)
                                    )
                                    pygame.draw.rect(
                                        self.WIN, (0, 0, 0), el.colision, 4
                                    )
                                    self.WIN.blit(
                                        text, (el.colision.x, el.colision.y - 25)
                                    )
                            if el.type == "colision":
                                el.colision.x = (
                                    el.x - el.colisionsizex / 2 + el.parent.x
                                )
                                el.colision.y = (
                                    el.y - el.colisionsizey / 2 + el.parent.y
                                )
                                el.colision.w = el.colisionsizex
                                el.colision.h = el.colisionsizey
                                if el.showcolision or self.devmode:
                                    text = self.font_fps.render(
                                        "ID: " + el.id, True, (0, 0, 0)
                                    )
                                    pygame.draw.rect(
                                        self.WIN, (0, 0, 0), el.colision, 4
                                    )
                                    self.WIN.blit(
                                        text, (el.colision.x, el.colision.y - 25)
                                    )
                            if el.type == "rect":
                                el.colision.x = el.x - el.w / 2 + el.parent.x
                                el.colision.y = el.y - el.h / 2 + el.parent.y
                                el.colision.w = el.w
                                el.colision.h = el.h
                                pygame.draw.rect(
                                    self.WIN, el.color, el.colision, el.border
                                )
                    else:
                        if el.type == "element":
                            self.WIN.blit(
                                el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                            )
                        if el.type == "entity":
                            self.WIN.blit(
                                el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                            )
                            el.colision.x = (
                                el.x + el.colisionoffsetx - el.colisionsizex / 2
                            )
                            el.colision.y = (
                                el.y + el.colisionoffsety - el.colisionsizey / 2
                            )
                            if el.showcolision or self.devmode:
                                text = self.font_fps.render(
                                    "ID: " + el.id, True, (0, 0, 0)
                                )
                                pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                                self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                        if el.type == "colision":
                            el.colision.x = el.x - el.colisionsizex / 2
                            el.colision.y = el.y - el.colisionsizey / 2
                            el.colision.w = el.colisionsizex
                            el.colision.h = el.colisionsizey
                            if el.showcolision or self.devmode:
                                text = self.font_fps.render(
                                    "ID: " + el.id, True, (0, 0, 0)
                                )
                                pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                                self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                        if el.type == "rect":
                            el.colision.x = el.x - el.w / 2
                            el.colision.y = el.y - el.h / 2
                            el.colision.w = el.w
                            el.colision.h = el.h
                            pygame.draw.rect(self.WIN, el.color, el.colision, el.border)
            except Exception as err:
                print(err)
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
