import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.locals import *
import time
from numba import jit
from numba import int32, float32  # import the types
from numba.experimental import jitclass
import pygame_gui

print("Hello From Panik Studios\nWelcome to Panik-Core Engine V0.0.5")

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.font.init()
pygame.init()


class Window:
    def __init__(self, title, width, height, icon=None):
        self.title = title
        self.width = width
        self.devmode = False
        self.showfps = False
        self.height = height
        self.icon = icon
        self.bg = (255, 255, 255)
        self.queue = []
        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        if self.icon:
            pygame.display.set_icon(pygame.image.load(icon).convert_alpha())
        # fps
        self.clock = pygame.time.Clock()
        self.font_fps = pygame.font.Font(None, 20)
        self.starttime = 0.0
        self.endtime = 0.0
        self.delta_time = 0.0

    @property
    def winsize(self):
        return pygame.display.get_surface().get_size()

    def blit(self, surface=[]):
        self.queue.extend(surface)

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
                    if el.type == "bigmap":
                        self.WIN.blit(
                            el.image,
                            (
                                0,
                                0,
                            ),
                            pygame.Rect(
                                (el.x - el.size_x / 2 + el.parent.x) * -1,
                                (el.y - el.size_y / 2 + el.parent.y) * -1,
                                self.winsize[0],
                                self.winsize[1],
                            ),
                        )
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
                        if el.showcolision and self.devmode:
                            text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                            pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                            self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
            else:
                if el.type == "bigmap":
                    self.WIN.blit(
                        el.image,
                        (
                            el.x - el.size_x / 2,
                            el.y - el.size_y / 2,
                        ),
                        pygame.Rect(
                            (el.x - el.size_x / 2 + el.parent.x) * -1,
                            (el.y - el.size_y / 2 + el.parent.y) * -1,
                            self.winsize[0],
                            self.winsize[1],
                        ),
                    )
                if el.type == "element":
                    self.WIN.blit(
                        el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                    )
                if el.type == "entity":
                    self.WIN.blit(
                        el.image, (el.x - el.size_x / 2, el.y - el.size_y / 2)
                    )
                    if el.showcolision and self.devmode:
                        text = self.font_fps.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                if el.type == "colision":
                    el.colision.x = el.x - el.colisionsizex / 2
                    el.colision.y = el.y - el.colisionsizey / 2
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


class Events:
    def __init__(self):
        self.QUIT = pygame.QUIT
        self.BUTTON_CLICKED = pygame_gui.UI_BUTTON_PRESSED
        self.BUTTON_DOUBLE_CLICKED = pygame_gui.UI_BUTTON_DOUBLE_CLICKED
        self.BUTTON_START_PRESS = pygame_gui.UI_BUTTON_START_PRESS
        self.BUTTON_HOVERED = pygame_gui.UI_BUTTON_ON_HOVERED
        self.BUTTON_UNHOVERED = pygame_gui.UI_BUTTON_ON_UNHOVERED
        self.TEXT_BOX_LINK_CLICKED = pygame_gui.UI_TEXT_BOX_LINK_CLICKED
        self.TEXT_ENTRY_CHANGED = pygame_gui.UI_TEXT_ENTRY_CHANGED
        self.TEXT_ENTRY_FINISHED = pygame_gui.UI_TEXT_ENTRY_FINISHED
        self.DROP_DOWN_MENU_CHANGED = pygame_gui.UI_DROP_DOWN_MENU_CHANGED
        self.HORIZONTAL_SLIDER_MOVED = pygame_gui.UI_HORIZONTAL_SLIDER_MOVED
        self.SELECTION_LIST_NEW_SELECTION = pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
        self.SELECTION_LIST_REMOVE_SELECTION = (
            pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION
        )
        self.SELECTION_LIST_DOUBLE_SELECT = (
            pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION
        )
        self.DIALOG_CONFIRMED = pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED
        self.PATH_SELECTED = pygame_gui.UI_FILE_DIALOG_PATH_PICKED
        self.WINDOW_CLOSED = pygame_gui.UI_WINDOW_CLOSE
        self.KEY_PRESSED = pygame.KEYDOWN
        self.SCREENRESIZE = pygame.VIDEORESIZE

    def get(self):
        return pygame.event.get()


class Game:
    def __init__(self):
        pass

    def quit(self):
        pygame.quit()


class Image:
    def __init__(self, path):
        self.image = pygame.image.load(path).convert_alpha()


class Animation:
    def __init__(self, animpath):
        self.animations = {}
        for filename in os.listdir(animpath):
            if filename.endswith(".png"):
                path = os.path.join(animpath, filename)
                key = filename[:-4]
                self.animations[key] = pygame.image.load(path).convert_alpha()


class BigMap:
    def __init__(
        self,
        id,
        image,
        x,
        y,
        image_scale=100,
        rotation=0,
        flip=[False, False],
        parent=False,
    ):
        self.id = id
        self.animationidx = 0
        self.starttime = time.time()
        self.parent = parent
        self.image_scale = image_scale
        self.flip = flip
        self.x, self.y = x, y
        self.rotation = rotation
        self.type = "bigmap"
        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image
        self.size_x = self.image_scale * self.image.get_width() / 100
        self.size_y = self.image_scale * self.image.get_height() / 100
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )

    def animate(self, animation, animname=None, delay=0.1):
        if animname:
            self.image = animation.animations[animname]
            self.size_x, self.size_y = (
                self.image_scale * self.image.get_width() / 100,
                self.image_scale * self.image.get_height() / 100,
            )
            self.image = pygame.transform.flip(
                pygame.transform.rotate(
                    pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                    self.rotation,
                ),
                self.flip[0],
                self.flip[1],
            )
        else:
            if time.time() - self.starttime > delay:
                self.starttime = time.time()
                if self.animationidx >= len(animation.animations) - 1:
                    self.animationidx = 0
                else:
                    self.animationidx += 1
                self.image = list(animation.animations.values())[self.animationidx]
                self.size_x, self.size_y = (
                    self.image_scale * self.image.get_width() / 100,
                    self.image_scale * self.image.get_height() / 100,
                )
                self.image = pygame.transform.flip(
                    pygame.transform.rotate(
                        pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                        self.rotation,
                    ),
                    self.flip[0],
                    self.flip[1],
                )

    def setImage(self):
        if type(self.image) == str:
            self.image = pygame.image.load(self.image).convert_alpha()
        self.size_x, self.size_y = (
            self.image_scale * self.image.get_width() / 100,
            self.image_scale * self.image.get_height() / 100,
        )
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )


class Element:
    def __init__(
        self,
        id,
        image,
        x,
        y,
        image_scale=100,
        rotation=0,
        flip=[False, False],
        parent=False,
    ):
        self.id = id
        self.animationidx = 0
        self.starttime = time.time()
        self.parent = parent
        self.image_scale = image_scale
        self.flip = flip
        self.x, self.y = x, y
        self.rotation = rotation
        self.type = "element"
        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image
        self.size_x = self.image_scale * self.image.get_width() / 100
        self.size_y = self.image_scale * self.image.get_height() / 100
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )

    def animate(self, animation, animname=None, delay=0.1):
        if animname:
            self.image = animation.animations[animname]
            self.size_x, self.size_y = (
                self.image_scale * self.image.get_width() / 100,
                self.image_scale * self.image.get_height() / 100,
            )
            self.image = pygame.transform.flip(
                pygame.transform.rotate(
                    pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                    self.rotation,
                ),
                self.flip[0],
                self.flip[1],
            )
        else:
            if time.time() - self.starttime > delay:
                self.starttime = time.time()
                if self.animationidx >= len(animation.animations) - 1:
                    self.animationidx = 0
                else:
                    self.animationidx += 1
                self.image = list(animation.animations.values())[self.animationidx]
                self.size_x, self.size_y = (
                    self.image_scale * self.image.get_width() / 100,
                    self.image_scale * self.image.get_height() / 100,
                )
                self.image = pygame.transform.flip(
                    pygame.transform.rotate(
                        pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                        self.rotation,
                    ),
                    self.flip[0],
                    self.flip[1],
                )

    def setImage(self):
        if type(self.image) == str:
            self.image = pygame.image.load(self.image).convert_alpha()
        self.size_x, self.size_y = (
            self.image_scale * self.image.get_width() / 100,
            self.image_scale * self.image.get_height() / 100,
        )
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )


class Entity:
    def __init__(
        self,
        id,
        image,
        x,
        y,
        image_scale=100,
        rotation=0,
        flip=[False, False],
        parent=False,
        colisionoffsetx=0,
        colisionoffsety=0,
        colisionsizex=100,
        colisionsizey=100,
    ):
        self.id = id
        self.animationidx = 0
        self.starttime = time.time()
        self.parent = parent
        self.image_scale = image_scale
        self.flip = flip
        self.x, self.y = x, y
        self.rotation = rotation
        self.type = "entity"
        self.showcolision = True
        if type(image) == str:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.image
        self.size_x = self.image_scale * self.image.get_width() / 100
        self.size_y = self.image_scale * self.image.get_height() / 100
        self.colisionoffsetx = colisionoffsetx
        self.colisionoffsety = colisionoffsety
        self.colisionsizex = colisionsizex
        self.colisionsizey = colisionsizey
        self.colision = pygame.Rect(
            self.x + colisionoffsetx - colisionsizex / 2,
            self.y + colisionoffsety - colisionsizey / 2,
            colisionsizex,
            colisionsizey,
        )
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )

    def moveX(self, x):
        self.x += x
        self.colision.x += x

    def moveY(self, y):
        self.y += y
        self.colision.y += y

    def tryMoveX(self, x, colisions=[]):
        self.x += x
        self.colision.x += x
        if self.isColidingGroup(colisions):
            self.x -= x
            self.colision.x -= x

    def tryMoveY(self, y, colisions=[]):
        self.y += y
        self.colision.y += y
        if self.isColidingGroup(colisions):
            self.y -= y
            self.colision.y -= y

    def isColidingGroup(self, colisiongroup=[]):
        if self.colision.collidelist(colisiongroup):
            return True
        return False

    def isColiding(self, colision):
        return pygame.Rect.colliderect(self.colision, colision.colision)

    def updatePosition(self):
        self.colision.x, self.colision.y = (
            self.x - self.size_x / 2 + self.parent.x,
            self.y - self.size_y / 2 + self.parent.y,
        )

    def animate(self, animation, animname=None, delay=0.1):
        if animname:
            self.image = animation.animations[animname]
            self.size_x, self.size_y = (
                self.image_scale * self.image.get_width() / 100,
                self.image_scale * self.image.get_height() / 100,
            )
            self.image = pygame.transform.flip(
                pygame.transform.rotate(
                    pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                    self.rotation,
                ),
                self.flip[0],
                self.flip[1],
            )
        else:
            if time.time() - self.starttime > delay:
                self.starttime = time.time()
                if self.animationidx >= len(animation.animations) - 1:
                    self.animationidx = 0
                else:
                    self.animationidx += 1
                self.image = list(animation.animations.values())[self.animationidx]
                self.size_x, self.size_y = (
                    self.image_scale * self.image.get_width() / 100,
                    self.image_scale * self.image.get_height() / 100,
                )
                self.image = pygame.transform.flip(
                    pygame.transform.rotate(
                        pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                        self.rotation,
                    ),
                    self.flip[0],
                    self.flip[1],
                )

    def setImage(self):
        if type(self.image) == str:
            self.image = pygame.image.load(self.image).convert_alpha()
        self.size_x, self.size_y = (
            self.image_scale * self.image.get_width() / 100,
            self.image_scale * self.image.get_height() / 100,
        )
        self.image = pygame.transform.flip(
            pygame.transform.rotate(
                pygame.transform.scale(self.image, (self.size_x, self.size_y)),
                self.rotation,
            ),
            self.flip[0],
            self.flip[1],
        )


class Colision:
    def __init__(
        self,
        id,
        colisionposx=0,
        colisionposy=0,
        colisionsizex=100,
        colisionsizey=100,
        parent=False,
    ):
        self.id = id
        self.x = colisionposx
        self.y = colisionposy
        self.colisionsizex = colisionsizex
        self.colisionsizey = colisionsizey
        self.parent = parent
        self.type = "colision"
        self.showcolision = True
        self.colision = pygame.Rect(
            colisionposx - colisionsizex / 2,
            colisionposy - colisionsizey / 2,
            colisionsizex,
            colisionsizey,
        )

    def moveX(self, x):
        self.x += x
        self.colision.x += x

    def moveY(self, y):
        self.y += y
        self.colision.y += y

    def isColiding(self, colision):
        return pygame.Rect.colliderect(self.colision, colision.colision)


class Parent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = "parent"
        self.hide = False


class ScrollParent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = "scrollparent"
        self.hide = False

    def isPlayerColiding(self, player, colisiongroup=[]):
        for col in colisiongroup:
            if pygame.Rect.colliderect(player.colision, col.colision):
                return True
        return False


class Mouse:
    def __init__(self):
        pass

    def getMousePos(self):
        return pygame.mouse.get_pos()

    @property
    def mousex(self):
        return pygame.mouse.get_pos()[0]

    @property
    def mousey(self):
        return pygame.mouse.get_pos()[1]

    def leftClick(self):
        return pygame.mouse.get_pressed()[0]

    def middleClick(self):
        return pygame.mouse.get_pressed()[1]

    def rightClick(self):
        return pygame.mouse.get_pressed()[3]

    def isColisionClicked(self, colision):
        if (
            pygame.Rect.colliderect(
                colision.colision, pygame.Rect((self.mousex, self.mousey), (1, 1))
            )
            and self.leftClick()
        ):
            return True
        return False


class Audio:
    def __init__(self):
        self.volume = 100

    def startAudio(self, path, volume=100, loop=-1):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume / 100)
        pygame.mixer.music.play(loop)

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume / 100)

    def increaseVol(self, v):
        self.setVolume(min(255, pygame.mixer.music.get_volume() + v))

    def decreaseVol(self, v):
        self.setVolume(max(0, pygame.mixer.music.get_volume() - v))

    def mute(self):
        pygame.mixer.music.set_volume(0.0)

    def unmute(self):
        global volume_
        pygame.mixer.music.set_volume(volume_ / 100)

    def toggleMute(self):
        if pygame.mixer.music.get_volume() == 0.0:
            self.unmute()
        else:
            self.mute()

    def playAudio(self, path):
        sound = pygame.mixer.Sound(path)
        sound.play()


class Keys:
    def __init__(self):
        self.kA = pygame.K_a
        self.kB = pygame.K_b
        self.kC = pygame.K_c
        self.kD = pygame.K_d
        self.kE = pygame.K_e
        self.kF = pygame.K_f
        self.kG = pygame.K_g
        self.kH = pygame.K_h
        self.kI = pygame.K_i
        self.kJ = pygame.K_j
        self.kK = pygame.K_k
        self.kL = pygame.K_l
        self.kM = pygame.K_m
        self.kN = pygame.K_n
        self.kO = pygame.K_o
        self.kP = pygame.K_p
        self.kQ = pygame.K_q
        self.kR = pygame.K_r
        self.kS = pygame.K_s
        self.kT = pygame.K_t
        self.kU = pygame.K_u
        self.kV = pygame.K_v
        self.kW = pygame.K_w
        self.kX = pygame.K_x
        self.kY = pygame.K_y
        self.kZ = pygame.K_z
        self.kUP = pygame.K_UP
        self.kLEFT = pygame.K_LEFT
        self.kDOWN = pygame.K_DOWN
        self.kRIGHT = pygame.K_RIGHT
        self.kTAB = pygame.K_TAB
        self.kSHIFT = pygame.K_LSHIFT
        self.kESC = pygame.K_ESCAPE
        self.kSPACE = pygame.K_SPACE
        self.kCTRL = pygame.K_LCTRL
        self.k0 = pygame.K_0
        self.k1 = pygame.K_1
        self.k2 = pygame.K_2
        self.k3 = pygame.K_3
        self.k4 = pygame.K_4
        self.k5 = pygame.K_5
        self.k6 = pygame.K_6
        self.k7 = pygame.K_7
        self.k8 = pygame.K_8
        self.k9 = pygame.K_9

    def getKeys(self):
        return pygame.key.get_pressed()


# ------------------- UI --------------------#
class UI:
    def __init__(self):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.loader = pygame_gui.core.IncrementalThreadedResourceLoader()
        self.manager = pygame_gui.UIManager(
            (self.w, self.h), resource_loader=self.loader
        )

    def update(self):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.w, self.h))

    def process_events(self, event):
        try:
            self.manager.process_events(event)
        except Exception as e:
            print(e)

    def set_size(self, sx, sy):
        self.manager.set_window_resolution((sx, sy))


class UIButton:
    def __init__(self, text, manager, x, y, sizex=100, sizey=50, container=None):
        self.container = container
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UIButton(
            relative_rect=self.colision,
            text=self.text,
            manager=self.manager.manager,
            allow_double_clicks=True,
            container=self.container,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIText:
    def __init__(self, text, manager, x, y, sizex=200, sizey=100, container=None):
        self.container = container
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UITextBox(
            self.text, self.colision, self.manager.manager, container=self.container
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UILabel:
    def __init__(self, text, manager, x, y, sizex=400, sizey=100, container=None):
        self.container = container
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UILabel(
            self.colision,
            self.text,
            self.manager.manager,
            container=self.container,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UITextEntry:
    def __init__(self, text, manager, x, y, sizex=200, sizey=50, container=None):
        self.container = container
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((x, y), (sizex, sizey))
        self.element = pygame_gui.elements.UITextEntryLine(
            self.colision, self.manager.manager, container=self.container
        )
        self.element.set_text(text)

    @property
    def input(self):
        return self.element.get_text()

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UICredEntry:
    def __init__(self, text, manager, x, y, sizex=200, sizey=50, container=None):
        self.container = container
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((x, y), (sizex, sizey))
        self.element = pygame_gui.elements.UITextEntryLine(
            self.colision, self.manager.manager, container=self.container
        )
        self.element.set_text(text)
        self.element.set_text_hidden(True)

    @property
    def input(self):
        return self.element.get_text()

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIDropDownMenu:
    def __init__(
        self,
        options,
        default_option,
        manager,
        x,
        y,
        sizex=100,
        sizey=25,
        container=None,
    ):
        self.container = container
        self.options = options
        self.default_option = default_option
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UIDropDownMenu(
            self.options,
            self.default_option,
            self.colision,
            self.manager.manager,
            container=self.container,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIHorizontalSlider:
    def __init__(
        self,
        manager,
        x,
        y,
        sizex=200,
        sizey=25,
        starting_value=0,
        range=(0, 100),
        container=None,
    ):
        self.container = container
        self.range = range
        self.starting_value = starting_value
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UIHorizontalSlider(
            self.colision,
            self.starting_value,
            self.range,
            self.manager.manager,
            container=self.container,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UISelectionList:
    def __init__(
        self, options, default, manager, x, y, sizex=200, sizey=200, container=None
    ):
        self.container = container
        self.options = options
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UISelectionList(
            self.colision,
            self.options,
            self.manager.manager,
            container=self.container,
            default_selection=default,
        )

    @property
    def selection(self):
        return self.element.get_single_selection()

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UICheckList:
    def __init__(self, options, manager, x, y, sizex=200, sizey=200, container=None):
        self.container = container
        self.options = options
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UISelectionList(
            self.colision,
            self.options,
            self.manager.manager,
            allow_multi_select=True,
            allow_double_clicks=False,
            container=self.container,
        )

    @property
    def selection(self):
        return self.element.get_multi_selection()

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIImage:
    def __init__(self, image, manager, x, y, sx, sy, container=None):
        self.colision = pygame.Rect((x, y), (sx, sy))
        self.surf = pygame.image.load(image).convert_alpha()
        self.image = pygame_gui.elements.UIImage(
            self.colision, self.surf, manager.manager, container
        )


class UIConfirmationDialog:
    def __init__(self, title, text, manager, x, y, sizex=260, sizey=200, priority=True):
        self.text = text
        self.title = title
        self.priority = priority
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.windows.UIConfirmationDialog(
            self.colision,
            self.manager.manager,
            self.text,
            window_title=self.title,
            blocking=self.priority,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIFileDialog:
    def __init__(
        self,
        title,
        initial_path,
        manager,
        x,
        y,
        sizex=600,
        sizey=400,
        allow_existing_files_only=False,
        allow_picking_directories=False,
    ):
        self.initial_path = initial_path
        self.title = title
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.windows.UIFileDialog(
            self.colision,
            self.manager.manager,
            self.title,
            self.initial_path,
            allow_existing_files_only=allow_existing_files_only,
            allow_picking_directories=allow_picking_directories,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIWindow:
    def __init__(
        self,
        title,
        manager,
        x,
        y,
        sizex=600,
        sizey=400,
        resizable=False,
    ):
        self.resizable = resizable
        self.title = title
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UIWindow(
            self.colision, self.manager.manager, self.title, resizable=resizable
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIContainer:
    def __init__(self, manager, x, y, sizex=600, sizey=400, container=None):
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UIScrollingContainer(
            self.colision,
            manager.manager,
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)


class UIPanel:
    def __init__(self, manager, x, y, sizex=600, sizey=400, container=None):
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.colision = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.element = pygame_gui.elements.UIPanel(
            self.colision, 1, manager.manager, container=container
        )

    def hide(self):
        self.element.hide()

    def show(self):
        self.element.show()

    def disable(self):
        self.element.disable()

    def enable(self):
        self.element.enable()

    def draw(self, delta):
        self.element.update(delta)
