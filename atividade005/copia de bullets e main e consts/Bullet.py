# Classe para o projétil
import pygame
import sys

class Bullet:
    def __init__(self, x, y, width, height, speed):
        self.image = pygame.image.load('assets/Bullet/bala.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect().copy()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.x += self.speed * self.rect.x
        self.rect.y += self.speed * self.rect.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)