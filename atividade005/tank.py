import pygame
from projectile import Projectile

class Tank:
    def __init__(self, x, y, color, is_player=True):
        self.rect = pygame.Rect(x, y, 50, 30)  #tank is a rectangle at the moment
        self.color = color
        self.speed = 5
        self.is_player = is_player
        self.cooldown = 0
        self.cooldown_time = 30  #shots frame
        self.direction = 1 if is_player else -1

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def move(self, keys):
        if self.is_player:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < 800:  #screen width
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < 600:  #screen height
                self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = self.cooldown_time
            return Projectile(self.rect.centerx, self.rect.centery, self.direction)
        return None