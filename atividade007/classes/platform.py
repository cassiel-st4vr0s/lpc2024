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
        self.platforms = []
        self.platform_typeA = pygame.image.load('assets\sprites\cloud_A.png')
        self.platform_typeA = pygame.transform.scale(self.platform_typeA, (PLATFORM_WIDTH + 20, PLATFORM_HEIGHT + 60))
        self.cloud_mask = pygame.mask.from_surface(self.platform_typeA)
        self.outline_pixels = self.cloud_mask.outline()
        self.cloud_outline = pygame.image.load('assets\sprites\cloud_A.png')
        self.cloud_outline.set_colorkey((0, 0, 0))



    def is_text_match(self):
        return self.typed == self.text