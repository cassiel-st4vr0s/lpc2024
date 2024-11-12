import pygame
from classes.gameloop import *
pygame.init()

#variables
combinations_size = 4 #controla a quantidade maxima de elementos agrupados
letters_1 = ['f','j'] #controla as letras combinadas
letters_2 = ['a','s','d','f','g']
letters_3 = ['h','j','k','l','ç']

if __name__ == "__main__":
    gameLoop = GameLoop()
    gameLoop.run()
