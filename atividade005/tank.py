import pygame

class Tank:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 30)
        self.color = color
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top <=0 or self.rect.bottom >= 600: #screen height
            self.speed = -self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def shoot(self):
        print("Tank Fired")