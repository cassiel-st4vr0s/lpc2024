import pygame
import sys
from tank import Tank
from projectile import Projectile

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

#enemy tank fire rate
ENEMY_FIRE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_FIRE_EVENT, 2000)  #2 segundos

projectiles = []
class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(self, x, y, width, height)

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
                new_projectile = player_tank.shoot()
                if new_projectile:
                    projectiles.append(new_projectile)
        if event.type == ENEMY_FIRE_EVENT:
            new_projectile = Projectile(enemy_tank.rect.centerx, enemy_tank.rect.centery, -1)
            if new_projectile:
                projectiles.append(new_projectile)



    #hanndle key press
    keys = pygame.key.get_pressed()
    player_tank.move(keys)

    #updates(game objetcs)
    player_tank.update()
    enemy_tank.update()

    for projectile in projectiles[:]:
        projectile.update()
        if projectile.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            projectiles.remove(projectile)

    #draw
    screen.fill(BLACK)
    player_tank.draw(screen)
    enemy_tank.draw(screen)
    for projectile in projectiles:
        projectile.draw(screen)

    pygame.display.flip()
    clock.tick(60)#fps

pygame.quit()
sys.exit()