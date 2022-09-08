import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import time
import pygame_gui
import pygame_texteditor

print("Hello From Panik Studios\nWelcome to Panik-Core Engine V0.1.0")

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
        self.queue = []
        self.BG = (255, 255, 255)
        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        if self.icon:
            pygame.display.set_icon(pygame.image.load(icon).convert_alpha())
        # fps
        self.clock = pygame.time.Clock()

    def blit(self, surface=[]):
        self.queue.extend(surface)

    def tick(self, fps=30):
        self.delta_time = self.clock.tick(fps) / 1000.0
        return self.delta_time

    def update(self, uimanager=None, ui=None):
        self.WIN.fill(self.BG)
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
                            font = pygame.font.Font(None, 30)
                            text = font.render("ID: " + el.id, True, (0, 0, 0))
                            pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                            self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                    if el.type == "colision":
                        el.colision.x = el.x - el.colisionsizex / 2 + el.parent.x
                        el.colision.y = el.y - el.colisionsizey / 2 + el.parent.y
                        if el.showcolision and self.devmode:
                            font = pygame.font.Font(None, 30)
                            text = font.render("ID: " + el.id, True, (0, 0, 0))
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
                    if el.showcolision and self.devmode:
                        font = pygame.font.Font(None, 30)
                        text = font.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
                if el.type == "colision":
                    el.colision.x = el.x - el.colisionsizex / 2
                    el.colision.y = el.y - el.colisionsizey / 2
                    if el.showcolision and self.devmode:
                        font = pygame.font.Font(None, 30)
                        text = font.render("ID: " + el.id, True, (0, 0, 0))
                        pygame.draw.rect(self.WIN, (0, 0, 0), el.colision, 4)
                        self.WIN.blit(text, (el.colision.x, el.colision.y - 25))
        self.queue = []
        # ui
        if uimanager:
            uimanager.manager.update(float(self.delta_time))
            uimanager.manager.draw_ui(self.WIN)
        if ui:
            for el in ui:
                el.draw(self.delta_time)
        if self.showfps:
            font = pygame.font.Font(None, 20)
            text = font.render(
                "FPS: " + str(round(self.clock.get_fps())), True, (0, 0, 0)
            )
            self.WIN.blit(text, (10, 15))
        pygame.display.update()

    def setResizable(self):
        self.WIN = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)


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
        self.KEY_PRESSED = pygame.KEYDOWN

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
        for col in colisiongroup:
            if pygame.Rect.colliderect(self.colision, col.colision):
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

    def leftClick(self):
        return pygame.mouse.get_pressed()[0]

    def middleClick(self):
        return pygame.mouse.get_pressed()[1]

    def rightClick(self):
        return pygame.mouse.get_pressed()[3]


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
        self.manager = pygame_gui.UIManager((self.w, self.h))

    def update(self):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.manager = pygame_gui.UIManager((self.w, self.h))

    def process_events(self, event):
        self.manager.process_events(event)


class UIButton:
    def __init__(self, text, manager, x, y, sizex=100, sizey=50):
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.button = pygame_gui.elements.UIButton(
            relative_rect=self.rect,
            text=self.text,
            manager=self.manager.manager,
            allow_double_clicks=True,
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.button = pygame_gui.elements.UIButton(
            relative_rect=self.rect,
            text=self.text,
            manager=self.manager.manager,
            allow_double_clicks=True,
        )

    def hide(self):
        self.button.hide()

    def show(self):
        self.button.show()

    def disable(self):
        self.button.disable()

    def enable(self):
        self.button.enable()

    def draw(self, delta):
        self.button.update(delta)


class UIText:
    def __init__(self, text, manager, x, y, sizex=200, sizey=100):
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.text = pygame_gui.elements.UITextBox(
            self.text, self.rect, self.manager.manager
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.text = pygame_gui.elements.UITextBox(
            self.text, self.rect, self.manager.manager
        )

    def hide(self):
        self.text.hide()

    def show(self):
        self.text.show()

    def disable(self):
        self.text.disable()

    def enable(self):
        self.text.enable()

    def draw(self, delta):
        self.text.update(delta)


class UILabel:
    def __init__(self, text, manager, x, y, sizex=400, sizey=100):
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.text = pygame_gui.elements.UILabel(
            self.rect, self.text, self.manager.manager
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.text = pygame_gui.elements.UILabel(
            self.rect, self.text, self.manager.manager
        )

    def hide(self):
        self.text.hide()

    def show(self):
        self.text.show()

    def disable(self):
        self.text.disable()

    def enable(self):
        self.text.enable()

    def draw(self, delta):
        self.text.update(delta)


class UITextEntry:
    def __init__(self, text, manager, x, y, sizex=200, sizey=50):
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((x, y), (sizex, sizey))
        self.textentry = pygame_gui.elements.UITextEntryLine(
            self.rect, self.manager.manager
        )
        self.textentry.set_text(text)

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.textentry = pygame_gui.elements.UITextEntryLine(
            self.rect, self.manager.manager
        )
        self.textentry.set_text(self.text)

    @property
    def input(self):
        return self.textentry.get_text()

    def hide(self):
        self.textentry.hide()

    def show(self):
        self.textentry.show()

    def disable(self):
        self.textentry.disable()

    def enable(self):
        self.textentry.enable()

    def draw(self, delta):
        self.textentry.update(delta)


class UICredEntry:
    def __init__(self, text, manager, x, y, sizex=200, sizey=50):
        self.text = text
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((x, y), (sizex, sizey))
        self.textentry = pygame_gui.elements.UITextEntryLine(
            self.rect, self.manager.manager
        )
        self.textentry.set_text(text)
        self.textentry.set_text_hidden(True)

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.textentry = pygame_gui.elements.UITextEntryLine(
            self.rect, self.manager.manager
        )
        self.textentry.set_text(self.text)
        self.textentry.set_text_hidden(True)

    @property
    def input(self):
        return self.textentry.get_text()

    def hide(self):
        self.textentry.hide()

    def show(self):
        self.textentry.show()

    def disable(self):
        self.textentry.disable()

    def enable(self):
        self.textentry.enable()

    def draw(self, delta):
        self.textentry.update(delta)


class UIDropDownMenu:
    def __init__(self, options, default_option, manager, x, y, sizex=100, sizey=25):
        self.options = options
        self.default_option = default_option
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.dropdownmenu = pygame_gui.elements.UIDropDownMenu(
            self.options, self.default_option, self.rect, self.manager.manager
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.dropdownmenu = pygame_gui.elements.UIDropDownMenu(
            self.options, self.default_option, self.rect, self.manager.manager
        )

    def hide(self):
        self.dropdownmenu.hide()

    def show(self):
        self.dropdownmenu.show()

    def disable(self):
        self.dropdownmenu.disable()

    def enable(self):
        self.dropdownmenu.enable()

    def draw(self, delta):
        self.dropdownmenu.update(delta)


class UIHorizontalSlider:
    def __init__(
        self, manager, x, y, sizex=200, sizey=25, starting_value=0, range=(0, 100)
    ):
        self.range = range
        self.starting_value = starting_value
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.slider = pygame_gui.elements.UIHorizontalSlider(
            self.rect, self.starting_value, self.range, self.manager.manager
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.slider = pygame_gui.elements.UIHorizontalSlider(
            self.rect, self.starting_value, self.range, self.manager.manager
        )

    def hide(self):
        self.slider.hide()

    def show(self):
        self.slider.show()

    def disable(self):
        self.slider.disable()

    def enable(self):
        self.slider.enable()

    def draw(self, delta):
        self.slider.update(delta)


class UISelectionList:
    def __init__(self, options, manager, x, y, sizex=200, sizey=200):
        self.options = options
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.selectionlist = pygame_gui.elements.UISelectionList(
            self.rect, self.options, self.manager.manager
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.selectionlist = pygame_gui.elements.UISelectionList(
            self.rect, self.options, self.manager.manager
        )

    @property
    def selection(self):
        return self.selectionlist.get_single_selection()

    def hide(self):
        self.selectionlist.hide()

    def show(self):
        self.selectionlist.show()

    def disable(self):
        self.selectionlist.disable()

    def enable(self):
        self.selectionlist.enable()

    def draw(self, delta):
        self.selectionlist.update(delta)


class UICheckList:
    def __init__(self, options, manager, x, y, sizex=200, sizey=200):
        self.options = options
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.selectionlist = pygame_gui.elements.UISelectionList(
            self.rect,
            self.options,
            self.manager.manager,
            allow_multi_select=True,
            allow_double_clicks=False,
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.selectionlist = pygame_gui.elements.UISelectionList(
            self.rect,
            self.options,
            self.manager.manager,
            allow_multi_select=True,
            allow_double_clicks=False,
        )

    @property
    def selection(self):
        return self.selectionlist.get_multi_selection()

    def hide(self):
        self.selectionlist.hide()

    def show(self):
        self.selectionlist.show()

    def disable(self):
        self.selectionlist.disable()

    def enable(self):
        self.selectionlist.enable()

    def draw(self, delta):
        self.selectionlist.update(delta)


class UIConfirmationDialog:
    def __init__(self, title, text, manager, x, y, sizex=260, sizey=200, priority=True):
        self.text = text
        self.title = title
        self.priority = priority
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex, sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.confirmdialog = pygame_gui.windows.UIConfirmationDialog(
            self.rect,
            self.manager.manager,
            self.text,
            window_title=self.title,
            blocking=self.priority,
        )

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
        self.confirmdialog = pygame_gui.windows.UIConfirmationDialog(
            self.rect,
            self.manager.manager,
            self.text,
            window_title=self.title,
            blocking=self.priority,
        )

    def hide(self):
        self.confirmdialog.hide()

    def show(self):
        self.confirmdialog.show()

    def disable(self):
        self.confirmdialog.disable()

    def enable(self):
        self.confirmdialog.enable()

    def draw(self, delta):
        self.confirmdialog.update(delta)


""" ------------------------------------------------------------------------------------ Work in progress
class UIWindow(pygame_gui.elements.UIWindow):
    def __init__(self, title, manager, x, y, sizex=400, sizey=600, resizable=False):
        super().__init__(pygame.Rect((x, y), (sizex, sizey)), manager.manager,
                         window_display_title=title, resizable=resizable)
        self.title = title
        self.elements = {}
        self.resizable = resizable
        self.manager = manager
        self.x, self.y, self.sizex, self.sizey = x, y, sizex,sizey
        self.rect = pygame.Rect((self.x, self.y), (self.sizex, self.sizey))
    
    def addElement(self, id, element):
        self.elements[id] = element
    
    def process_events(self, event):
        handled = super().process_event(event)
        return handled

    def hide(self):
        super().hide()
    
    def show(self):
        super().show()

    def disable(self):
       super().disable()
    
    def enable(self):
        super().enable()

    def draw(self, delta):
        super().update(delta)

class UIPWindow(pygame_gui.elements.UIWindow):
    def __init__(self, position, ui_manager):
        super().__init__(pygame.Rect(position, (320, 240)), ui_manager.manager,
                         window_display_title='Super Awesome Pong!',
                         object_id='#pong_window')

        self.button = pygame_gui.elements.UIButton(pygame.Rect((0, 0), (100, 50)), "Button", ui_manager.manager, container=self, parent_element=self)
        self.dropdown = pygame_gui.elements.UIDropDownMenu(["One", "Two", "Three"], "One", pygame.Rect((100, 0), (100, 25)), ui_manager.manager, container=self, parent_element=self)


        self.is_active = False

    def process_event(self, event):
        handled = super().process_event(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == "#pong_window.#title_bar" and
                event.ui_element == self.title_bar):
            handled = True
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
        if self.is_active:
            pass
        return handled

    def update(self, time_delta):
        if self.alive() and self.is_active:
            pass

        super().update(time_delta)
"""
