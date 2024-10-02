import pygame

class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)  # Simple square for the projectile
        self.speed = 7
        self.bounces = 0
    
    def update(self):
        # This will be implemented later
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)  # Yellow color for projectiles