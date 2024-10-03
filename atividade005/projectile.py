import pygame
class Projectile:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 10)  #projetile is a square at the moment
        self.speed = 7
        self.direction = direction #1 = right, -1 = left at the moment
    
    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)  #projectiles are yellow
    
    def is_off_screen(self, screen_width, screen_height):
        return self.rect.right < 0 or self.rect.left > screen_width or \
               self.rect.bottom < 0 or self.rect.top > screen_height