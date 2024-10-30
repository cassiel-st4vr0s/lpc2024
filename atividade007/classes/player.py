import pygame
from settings import PLAYER_SIZE, GRAVITY, SCREEN_HEIGHT, PLATFORM_WIDTH

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_y = y
        self.vel_y = 0
        self.jumping = False
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def update(self):
        if self.jumping:
            if abs(self.y - self.target_y) > 2:
                self.y += (self.target_y - self.y) * 0.1
            else:
                self.y = self.target_y
                self.jumping = False
        else:
            self.vel_y += GRAVITY
            self.y += self.vel_y
            if self.y > SCREEN_HEIGHT - PLAYER_SIZE:
                self.y = SCREEN_HEIGHT - PLAYER_SIZE
                self.vel_y = 0
        self.rect.y = self.y
        self.rect.x = self.x

    def jump_to_platform(self, platform):
        self.jumping = True
        self.target_y = platform.y - PLAYER_SIZE
        self.x = platform.x + (PLATFORM_WIDTH // 2) - (PLAYER_SIZE // 2)
        self.rect.x = self.x
        self.vel_y = 0
