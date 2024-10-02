import pygame
import sys
from tank import Tank


pygame.init()

#screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Tank Game")

#defining colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)

#tanks(player and ai enemy)
player_tank = Tank(100, SCREEN_HEIGHT // 2, WHITE)
enemy_tank = Tank(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, (255, 0, 0)) #enemy is red

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(self, x, y, width, height), self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

#game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                player_tank.shoot()

    #updates(game objetcs)
    player_tank.update()
    enemy_tank.update()

    #draw
    screen.fill(BLACK)
    player_tank.draw(screen)
    enemy_tank.draw(screen)

    pygame.display.flip()
    clock.tick(60)#fps

pygame.quit()
sys.exit()