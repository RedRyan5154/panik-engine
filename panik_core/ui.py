import pygame
import pygame_gui


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
