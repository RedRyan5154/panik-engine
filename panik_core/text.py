import pygame


class Text:
    def __init__(
        self,
        id,
        text,
        font=None,
        size=30,
        x=0,
        y=0,
        color=(0, 0, 0),
        parent=False,
    ):
        self.id = id
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.parent = parent
        self.type = "text"

    def updateText(self, text, color=(0, 0, 0), font=None):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
