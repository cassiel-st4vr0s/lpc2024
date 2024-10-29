import pygame
from classes.gameloop import *
import sys
pygame.init()



#variables
combinations_size = 2 #controla a quantidade maxima de elementos agrupados
letters = ['f','j'] #controla as letras combinadas

if __name__ == "__main__":
    gameLoop = GameLoop()
    gameLoop.run()
