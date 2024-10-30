import pygame
from settings import PLATFORM_WIDTH, PLATFORM_HEIGHT

class Platform:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.typed = ""
        self.completed = False
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def is_text_match(self):
        return self.typed == self.text