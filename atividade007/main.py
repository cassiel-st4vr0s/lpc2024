import pygame
from classes.gameloop import *

pygame.init()

#animation
last_update = pygame.time.get_ticks()
frame = 0
animation_cooldown = 300

#variables
combinations_size = 2 #controla a quantidade maxima de elementos agrupados
letters = ['f','j'] #controla as letras combinadas

if __name__ == "__main__":
    gameLoop = GameLoop()
    gameLoop.run()
